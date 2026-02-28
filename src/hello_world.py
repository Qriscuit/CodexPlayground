"""First executable script for the Layer-Aware Cleanup prototype."""

from os import getenv


def main() -> None:
    app_name = getenv("APP_NAME", "layer-aware-cleanup-prototype")
    app_env = getenv("APP_ENV", "development")

    print(f"Hello, world! {app_name} is running in the {app_env} environment.")


if __name__ == "__main__":
    main()
