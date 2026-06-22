import generate_data
import clean_data
import feature_engineering
import load_mysql

def main():

    print("STEP 1: Generating data...")
    generate_data.main()

    print("STEP 2: Cleaning data...")
    clean_data.main()

    print("STEP 3: Feature engineering...")
    feature_engineering.main()

    print("STEP 4: Loading into MySQL...")
    load_mysql.main()

    print("PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main() 