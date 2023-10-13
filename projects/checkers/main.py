from modules.args import main_arguments

def main():
    try:
        main_arguments()
    except Exception as err:
        raise Exception(f"E: {err}")

if __name__ == "__main__":
    main()