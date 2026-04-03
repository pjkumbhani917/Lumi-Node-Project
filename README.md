Lumi Node Project 🌱🚗
Lumi Node is an AI-powered traffic analysis tool designed to optimize traffic flow and calculate potential energy and emissions savings. Developed as part of the Skills4Future hackathon under the "Green Skills and AI" track, this project leverages computer vision to analyze vehicular movement and quantify the environmental benefits of traffic optimization.

🎯 Project Objective
Urban traffic congestion contributes significantly to unnecessary carbon emissions. Lumi Node uses real-time or recorded traffic data to track vehicle density and movement, translating that data into actionable insights for sustainable city planning and green energy savings.

🗂️ Repository Structure
app.py: The main application file (likely running a web framework like Streamlit or Flask) that serves the user interface and dashboard.

_lumi_node_analysis.ipynb: A Jupyter Notebook containing the core exploratory data analysis (EDA), model testing, and metric calculations.

yolov8n.pt: The pre-trained YOLOv8 Nano model weights used for fast and efficient object (vehicle) detection.

traffic_analysis.csv: Contains the raw or processed data regarding vehicle counts, types, and traffic flow.

hourly_summary.csv: Aggregated traffic data broken down by the hour for trend analysis.

savings_metrics.csv: The core "Green Skills" output—quantifying the estimated reduction in fuel consumption and CO2 emissions based on optimized traffic flow.

requirements.txt: List of all Python dependencies required to run the project.

🚀 Technologies Used
Python: Core programming language.

YOLOv8 (Ultralytics): Used for state-of-the-art, real-time object detection (identifying cars, trucks, buses, etc.).

Jupyter Notebook: For data processing and algorithm prototyping.

Pandas/NumPy: For data manipulation and aggregating the CSV metrics.

⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/pjkumbhani917/Lumi-Node-Project.git
cd Lumi-Node-Project
Set up a virtual environment (Recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
# If it is a Streamlit app:
streamlit run app.py

# If it is a standard Python script/Flask app:
python app.py
📊 How It Works
Detection: The YOLOv8 model (yolov8n.pt) processes video feeds to detect and count vehicles.

Analysis: The system analyzes this data to create an hourly_summary.csv and traffic_analysis.csv, identifying peak hours and congestion points.

Green Metrics: Finally, it calculates the environmental impact, outputting savings_metrics.csv to show how much fuel could be saved and emissions reduced if traffic flow were optimized.
