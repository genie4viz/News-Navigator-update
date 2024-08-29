# News Navigator

**News Navigator** is a web application that fetches and displays the latest news articles from various sources. It leverages the power of Python and Flask to create a dynamic and interactive news platform.

## Features

- **Automated News Fetching:** Automatically fetches the latest news articles from Google News RSS.
- **Real-time Updates:** Keeps the news feed updated with the latest articles.
- **Responsive Design:** Accessible on various devices, including desktops, tablets, and smartphones.
- **Vercel Deployment:** Easily deployable on Vercel for a smooth and scalable deployment experience.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel
- **Other Tools:** Google News RSS, Bootstrap

## Getting Started

### Prerequisites

- Python 3.12.5
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Zaidkhalid44/News-Navigator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd News-Navigator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Fetch the latest news:
   ```bash
   python fetch_news.py
   ```
2. Run the Flask server:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://localhost:5000` to see the application in action.

## Deployment

The application can be easily deployed to Vercel by following these steps:

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Deploy the application:
   ```bash
   vercel
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
