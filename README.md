# About
Convert NGINX standard file listing in pre tag to table with full hrefs and no text truncation

# Usage

1. Setup virtual environment and install required libraries
    ```
    sudo apt install python3.9-venv
    python3.9 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
    ```
2. Pass URL (served using standard NGINX file listing module ngx_http_autoindex_module) to script:
    ```
    python http:/your.path
    ```
URL will be parsed and saved to html file where:
1. `href` relative values will be converted to absolute ones.
2. `a` tag text will not be truncated (stupid default limitation https://github.com/nginx/nginx/blob/master/src/http/modules/ngx_http_autoindex_module.c#L53)
3. `a` tags in `pre` tag will be reformated to table for more conveninent browsing

