import pickle
import argparse

PCONF = 'pconf'

def pickle_data(usr, pwd, rec):
    data = {
        'pwd': pwd,
        'usr': usr,
        'rec': rec,
    }
    with open(PCONF, 'w') as f:
        pickle.dump(data, f)


def get_config_data():
    with open(PCONF, 'r') as f:
        data = pickle.load(f)
    return data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--usr')
    parser.add_argument('--pwd')
    parser.add_argument('--rec', nargs='+')
    args = parser.parse_args()
    usr = args.usr
    pwd = args.pwd
    rec = args.rec
    pickle_data(usr, pwd, rec)
    print get_config_data()