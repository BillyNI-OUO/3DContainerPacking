import argparse



if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-j", "--json-data", dest="json_data")
    args=parser.parse_args
    print("Hello json"+args.json_data)