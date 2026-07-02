import os

import generate_data
import clean_data
import feature_engineering

def main():

    print("STEP 1: Generating data...")
    generate_data.main()

    print("STEP 2: Cleaning data...")
    clean_data.main()

    print("STEP 3: Feature engineering...")
    feature_engineering.main()

    if os.getenv("LOAD_MYSQL", "false").lower() in {"1", "true", "yes"}:
        import load_mysql

        print("STEP 4: Loading into MySQL...")
        load_mysql.main()
    else:
        print("STEP 4: Skipping MySQL load. Set LOAD_MYSQL=true to enable it.")

    print("PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
