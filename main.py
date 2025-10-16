from spotify_auth import generate_auth_url, start_callback_server

def main():
    url = generate_auth_url()
    print(f'Go to this url\n: {url} \n')

    code = start_callback_server()
    print(f'\n\nYou got the code: \n{code}')


if __name__ == "__main__":
    main()
