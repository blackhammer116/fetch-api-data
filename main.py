from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import mysql.connector
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)
news_url = "https://newsapi.org/v2/top-headlines"


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/news", methods=["GET"])
def news():
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return jsonify({"error": "Missing API key"}), 400

    country = request.args.get("country")
    category = request.args.get("category")
    if not country or not category:
        country = request.args.get("country", "us")
        category = request.args.get("category", "general")

    params = {"apikey": NEWS_API_KEY, "country": country, "category": category}

    try:
        response = requests.get(news_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            return (
                jsonify({"error": data.get("message", "Unknown error from NewsAPI")}),
                400,
            )

        articles = data.get("articles", [])
        conn = get_db_connection()
        cursor = conn.cursor()

        for article in articles:
            title = article.get("title")
            description = article.get("description")
            url = article.get("url")
            published_at = article.get("publishedAt")

            published_dt = None
            if published_at:
                published_dt = datetime.fromisoformat(
                    published_at.replace("Z", "+00:00")
                )

            cursor.execute(
                """
                INSERT INTO articles (title, description, url, published_at)
                VALUES (%s, %s, %s, %s)
            """,
                (title, description, url, published_dt),
            )

        conn.commit()
        cursor.close()
        conn.close()

        # return jsonify({"message": f"{len(articles)} articles saved."})
        return jsonify({'articls': articles,
                        "message": f"{len(articles)} articles saved."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to send request, {str(e)}"}), 500
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unknown Error has occured, {str(e)}"}), 500


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
