# <b>Fetch API Data</b>
<p>This is a simple backend app to fetch news data from news api. The main purpose of this project is to test out the github workflow to run the test cases</p>

## <b>How it works</b>
<ol>
    <li>Clone the repo</li>
    <li>Move to project dir<br> ```cd fetch-api-data```</li>
    <li>Install dependencies<br>
    ```pip install -r requirements.txt``` 
    </li>
    <li>Create your DB using
    ```cat db.sql | mysql```
    </li>
    <li>Store your mysql user, pw, host and db_name inside your .env file</li>
    <li>Also store the API key inside the .env</li>
    <li>Run the server
    ```python main.py```
    </li>
</ol>
<p>To check, open another terminal and run the following code ```curl 127.0.0.1:5000/news```</p>