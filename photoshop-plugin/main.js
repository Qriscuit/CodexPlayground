const photoshop = require("photoshop");
const { app, core, action, imaging } = photoshop;
const { localFileSystem } = require("uxp").storage;
const { entrypoints } = require("uxp");

const DEFAULT_SERVICE_URL = "http://127.0.0.1:8765";

/**
 * @typedef {Object} LayerSnapshot
 * @property {number|string} document_id
 * @property {number|string} layer_id
 * @property {{left:number, top:number, width:number, height:number}} bounds
 * @property {string} color_mode
 * @property {number[]} rgba8
 * @property {string} source_hash
 */

/**
 * @typedef {Object} RepairProposal
 * @property {string} region_id
 * @property {{x:number, y:number, width:number, height:number}} bbox
 * @property {number} confidence
 * @property {{width:number, height:number, runs:number[][]}} mask_rle
 * @property {string} reason
 * @property {string[]} risk_tags
 */

/**
 * @typedef {Object} RepairSession
 * @property {string} session_id
 * @property {LayerSnapshot} snapshot
 * @property {RepairProposal[]} proposals
 * @property {string[]} selected_region_ids
 * @property {string} started_at
 * @property {number[]} result_layer_ids
 */

/**
 * @typedef {Object} AuditEntry
 * @property {string} session_id
 * @property {number|string} document_id
 * @property {number|string} source_layer_id
 * @property {string[]} accepted_region_ids
 * @property {RepairProposal[]} proposals
 * @property {number[]} result_layer_ids
 * @property {string} created_at
 */

const state = {
  serviceUrl: DEFAULT_SERVICE_URL,
  layerMap: new Map(),
  currentSession: null,
  previewVisible: true
};

function $(id) {
  return document.getElementById(id);
}

function setStatus(message) {
  $("status-line").textContent = message;
}

function setServiceStatus(message) {
  $("service-status").textContent = message;
}

function setAnalysisSummary(message) {
  $("analysis-summary").textContent = message;
}

function safeNumber(value) {
  if (typeof value === "number") {
    return Math.round(value);
  }
  if (value && typeof value === "object" && "_value" in value) {
    return Math.round(Number(value._value));
  }
  return Math.round(Number(value || 0));
}

function layerBoundsToRect(layerBounds) {
  if (!Array.isArray(layerBounds) || layerBounds.length < 4) {
    return { left: 0, top: 0, width: 0, height: 0 };
  }
  const left = safeNumber(layerBounds[0]);
  const top = safeNumber(layerBounds[1]);
  const right = safeNumber(layerBounds[2]);
  const bottom = safeNumber(layerBounds[3]);
  return {
    left,
    top,
    width: Math.max(0, right - left),
    height: Math.max(0, bottom - top)
  };
}

function isProbablyPixelLayer(layer) {
  if (!layer) {
    return false;
  }
  if (Array.isArray(layer.layers) && layer.layers.length > 0) {
    return false;
  }
  const kindString = String(layer.kind || "").toLowerCase();
  if (kindString.includes("pixel") || kindString.includes("normal")) {
    return true;
  }
  if (kindString.includes("text") || kindString.includes("adjustment") || kindString.includes("smart")) {
    return false;
  }
  return true;
}

function flattenLayers(layers, prefix = "") {
  const rows = [];
  for (const layer of layers || []) {
    const name = prefix ? `${prefix}/${layer.name}` : layer.name;
    if (Array.isArray(layer.layers) && layer.layers.length > 0) {
      rows.push(...flattenLayers(layer.layers, name));
      continue;
    }
    if (isProbablyPixelLayer(layer)) {
      rows.push({ id: layer.id, name, layer });
    }
  }
  return rows;
}

async function callService(path, method = "GET", payload = null) {
  const baseUrl = $("service-url").value.trim() || DEFAULT_SERVICE_URL;
  state.serviceUrl = baseUrl;
  const url = `${baseUrl}${path}`;
  const request = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };
  if (payload) {
    request.body = JSON.stringify(payload);
  }

  const response = await fetch(url, request);
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Service ${response.status}: ${body}`);
  }
  return response.json();
}

async function pingService() {
  try {
    const response = await callService("/health", "GET");
    setServiceStatus(`Connected: ${response.status} v${response.version}`);
    setStatus("Service connection ready.");
  } catch (error) {
    setServiceStatus(`Disconnected: ${error.message}`);
    setStatus("Start the local Python service and try again.");
  }
}

async function refreshLayers() {
  const select = $("layer-select");
  select.innerHTML = "";
  state.layerMap.clear();

  const doc = app.activeDocument;
  if (!doc) {
    setStatus("Open a Photoshop document first.");
    return;
  }

  const flattened = flattenLayers(doc.layers);
  if (flattened.length === 0) {
    setStatus("No pixel layers found in the active document.");
    return;
  }

  for (const row of flattened) {
    const option = document.createElement("option");
    option.value = String(row.id);
    option.textContent = row.name;
    select.appendChild(option);
    state.layerMap.set(String(row.id), row.layer);
  }

  setStatus(`Loaded ${flattened.length} candidate pixel layers.`);
}

function getSelectedLayer() {
  const id = $("layer-select").value;
  return state.layerMap.get(String(id));
}

async function readLayerSnapshot(layer) {
  const doc = app.activeDocument;
  if (!doc || !layer) {
    throw new Error("No active document/layer.");
  }

  const layerBounds = layerBoundsToRect(layer.bounds);
  if (layerBounds.width === 0 || layerBounds.height === 0) {
    throw new Error("Selected layer has empty bounds.");
  }

  const pixelsResult = await imaging.getPixels({
    documentID: doc.id,
    layerID: layer.id,
    sourceBounds: {
      left: layerBounds.left,
      top: layerBounds.top,
      right: layerBounds.left + layerBounds.width,
      bottom: layerBounds.top + layerBounds.height
    },
    componentSize: 8,
    applyAlpha: true
  });

  const imageData = pixelsResult.imageData;
  const buffer = imageData.getData ? await imageData.getData() : imageData.data;
  const rgba8 = Array.from(buffer);
  const sourceHash = hashRgba(rgba8);

  return {
    document_id: doc.id,
    layer_id: layer.id,
    bounds: layerBounds,
    color_mode: "RGBA8",
    rgba8,
    source_hash: sourceHash
  };
}

function hashRgba(values) {
  // FNV-1a 32-bit hash for light-weight session identity in panel state.
  let hash = 0x811c9dc5;
  for (const value of values) {
    hash ^= value & 0xff;
    hash = (hash * 0x01000193) >>> 0;
  }
  return `fnv32-${hash.toString(16).padStart(8, "0")}`;
}

function renderProposals(proposals) {
  const container = $("proposal-list");
  container.innerHTML = "";

  if (!proposals || proposals.length === 0) {
    container.textContent = "No candidate regions returned.";
    return;
  }

  for (const proposal of proposals) {
    const wrapper = document.createElement("div");
    wrapper.className = "proposal-item";

    const title = document.createElement("div");
    title.className = "proposal-title";
    title.innerHTML =
      `<label class="inline-checkbox"><input type="checkbox" data-region-id="${proposal.region_id}" checked />` +
      `${proposal.region_id} (${Math.round(proposal.confidence * 100)}%)</label>`;

    const meta = document.createElement("div");
    meta.className = "proposal-meta";
    const bbox = proposal.bbox || { x: 0, y: 0, width: 0, height: 0 };
    const risks = Array.isArray(proposal.risk_tags) && proposal.risk_tags.length > 0 ? proposal.risk_tags.join(", ") : "none";
    meta.textContent = `bbox=${bbox.x},${bbox.y},${bbox.width}x${bbox.height} | risks=${risks}`;

    wrapper.appendChild(title);
    wrapper.appendChild(meta);
    container.appendChild(wrapper);
  }
}

function collectSelectedRegionIds() {
  const checkboxes = document.querySelectorAll("input[data-region-id]");
  const selected = [];
  for (const checkbox of checkboxes) {
    if (checkbox.checked) {
      selected.push(checkbox.getAttribute("data-region-id"));
    }
  }
  return selected;
}

function makeSessionId() {
  const now = new Date();
  return `sess-${now.toISOString().replace(/[:.]/g, "-")}`;
}

async function analyzeLayer() {
  const layer = getSelectedLayer();
  if (!layer) {
    setStatus("Select a pixel layer before analysis.");
    return;
  }

  try {
    setStatus("Reading layer pixels...");
    const snapshot = await readLayerSnapshot(layer);
    const sessionId = makeSessionId();
    const response = await callService("/v1/detect", "POST", {
      session_id: sessionId,
      document_id: String(snapshot.document_id),
      layer_id: String(snapshot.layer_id),
      bounds: snapshot.bounds,
      rgba8: snapshot.rgba8,
      options: {
        contrast_threshold: 32,
        min_region_area: 2,
        max_region_fraction: 0.02,
        max_regions: 50
      }
    });

    state.currentSession = {
      session_id: response.session_id || sessionId,
      snapshot,
      proposals: response.proposals || [],
      selected_region_ids: [],
      started_at: new Date().toISOString(),
      result_layer_ids: []
    };

    renderProposals(state.currentSession.proposals);
    setAnalysisSummary(
      `${state.currentSession.proposals.length} proposals. Candidate pixels: ${response.stats?.candidate_pixel_count || 0}`
    );
    setStatus("Analysis complete. Review proposals and apply selected.");
  } catch (error) {
    setStatus(`Analyze failed: ${error.message}`);
  }
}

async function setLayerVisibility(layerId, visible) {
  await core.executeAsModal(async () => {
    await action.batchPlay(
      [
        {
          _obj: "set",
          _target: [{ _ref: "layer", _id: layerId }],
          to: {
            _obj: "layer",
            visible
          }
        }
      ],
      { synchronousExecution: true, modalBehavior: "execute" }
    );
  }, { commandName: "Toggle FlatMagic Preview" });
}

async function applyPixelsToLayer(layerId, bounds, rgba8) {
  const imageData = await imaging.createImageDataFromBuffer(Uint8Array.from(rgba8), {
    width: bounds.width,
    height: bounds.height,
    components: 4,
    chunky: true
  });

  await imaging.putPixels({
    documentID: app.activeDocument.id,
    layerID: layerId,
    imageData,
    targetBounds: {
      left: bounds.left,
      top: bounds.top,
      right: bounds.left + bounds.width,
      bottom: bounds.top + bounds.height
    },
    replace: true
  });
}

async function applySelected() {
  const session = state.currentSession;
  if (!session) {
    setStatus("Analyze a layer first.");
    return;
  }

  const selected = collectSelectedRegionIds();
  session.selected_region_ids = selected;
  if (selected.length === 0) {
    setStatus("No proposals selected.");
    return;
  }

  try {
    setStatus("Requesting repaired pixels from service...");
    const repairResponse = await callService("/v1/repair", "POST", {
      session_id: session.session_id,
      document_id: String(session.snapshot.document_id),
      layer_id: String(session.snapshot.layer_id),
      bounds: session.snapshot.bounds,
      rgba8: session.snapshot.rgba8,
      proposals: session.proposals,
      accepted_region_ids: selected,
      options: {
        blend_strength: 0.7
      },
      write_log: true
    });

    const sourceLayer = state.layerMap.get(String(session.snapshot.layer_id));
    if (!sourceLayer) {
      throw new Error("Source layer no longer available in active document.");
    }

    let resultLayerId = null;
    await core.executeAsModal(async () => {
      const duplicate = await sourceLayer.duplicate();
      duplicate.name = `${sourceLayer.name} - FlatMagic`;
      resultLayerId = duplicate.id;
      await applyPixelsToLayer(resultLayerId, session.snapshot.bounds, repairResponse.rgba8);
    }, { commandName: "Apply FlatMagic Repair" });

    session.result_layer_ids.push(resultLayerId);
    state.previewVisible = true;
    $("preview-toggle").checked = true;
    setStatus(
      `Applied ${selected.length} region(s). Changed pixels: ${repairResponse.repair_stats?.changed_pixel_count || 0}`
    );
  } catch (error) {
    setStatus(`Apply failed: ${error.message}`);
  }
}

async function rollbackSession() {
  const session = state.currentSession;
  if (!session || session.result_layer_ids.length === 0) {
    setStatus("No result layers to roll back.");
    return;
  }

  try {
    await core.executeAsModal(async () => {
      for (const layerId of session.result_layer_ids) {
        await action.batchPlay(
          [
            {
              _obj: "delete",
              _target: [{ _ref: "layer", _id: layerId }]
            }
          ],
          { synchronousExecution: true, modalBehavior: "execute" }
        );
      }
    }, { commandName: "Rollback FlatMagic Session" });

    session.result_layer_ids = [];
    setStatus("Session rollback complete.");
  } catch (error) {
    setStatus(`Rollback failed: ${error.message}`);
  }
}

async function exportAuditLog() {
  const session = state.currentSession;
  if (!session) {
    setStatus("No session to export.");
    return;
  }

  /** @type {AuditEntry} */
  const audit = {
    session_id: session.session_id,
    document_id: session.snapshot.document_id,
    source_layer_id: session.snapshot.layer_id,
    accepted_region_ids: session.selected_region_ids || [],
    proposals: session.proposals,
    result_layer_ids: session.result_layer_ids,
    created_at: new Date().toISOString()
  };

  try {
    const root = await localFileSystem.getDataFolder();
    let logsFolder;
    try {
      logsFolder = await root.getEntry("logs");
    } catch (_error) {
      logsFolder = await root.createFolder("logs");
    }
    const file = await logsFolder.createFile(`${session.session_id}.json`, { overwrite: true });
    await file.write(JSON.stringify(audit, null, 2));
    setStatus(`Audit exported to plugin data folder as ${file.name}.`);
  } catch (error) {
    setStatus(`Failed to export audit log: ${error.message}`);
  }
}

async function togglePreview() {
  const checked = $("preview-toggle").checked;
  state.previewVisible = checked;
  const session = state.currentSession;
  if (!session || session.result_layer_ids.length === 0) {
    return;
  }

  try {
    for (const layerId of session.result_layer_ids) {
      await setLayerVisibility(layerId, checked);
    }
  } catch (error) {
    setStatus(`Preview toggle failed: ${error.message}`);
  }
}

function wireUi() {
  $("service-url").value = state.serviceUrl;
  $("ping-service").addEventListener("click", () => {
    pingService();
  });
  $("refresh-layers").addEventListener("click", () => {
    refreshLayers();
  });
  $("analyze-layer").addEventListener("click", () => {
    analyzeLayer();
  });
  $("apply-selected").addEventListener("click", () => {
    applySelected();
  });
  $("rollback-session").addEventListener("click", () => {
    rollbackSession();
  });
  $("export-audit").addEventListener("click", () => {
    exportAuditLog();
  });
  $("preview-toggle").addEventListener("change", () => {
    togglePreview();
  });
}

async function initializePanel() {
  if (!window.__flatMagicPanelInitialized) {
    window.__flatMagicPanelInitialized = true;
    wireUi();
  }
  await pingService();
  await refreshLayers();
}

entrypoints.setup({
  panels: {
    flatmagicPanel: {
      show() {
        initializePanel().catch((error) => {
          setStatus(`Initialization failed: ${error.message}`);
        });
      }
    }
  }
});
