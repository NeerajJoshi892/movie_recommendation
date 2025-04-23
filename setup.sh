mkdir -p ~/.streamlit/

echo '\
[server]\n\
port = $PORT\N\
headless =  true\n\
\n\
">~/.streamlit/config.toml