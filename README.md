
## Prerequisites

- Python 3.x
- Flask

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```
2. **Enter the repo in terminal**:


3. **Set up a Python virtual environment**:
    ```bash
    python3 -m venv venv
    ```

4. **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```

5. **Install Flask**:
    ```bash
    pip install Flask
    ```

6. **Configure API Key**:
    - Create a file `config.js` in the `static/js` folder.
    - Add your Google Maps API Key in `config.js`:
      ```javascript
      const API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY';
      export default API_KEY;
      ```

7. **Run the Flask App**:
    ```bash
    python app.py
    ```

8. **Open your web browser** and navigate to `http://127.0.0.1:5000/` to see your application in action.

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment by running:
```bash
deactivate
