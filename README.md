# Face Recognition System

Welcome to the **Face Recognition System**! 🎭

This application leverages OpenCV and Face Recognition for real-time facial detection. It identifies and processes faces instantly, offering users the flexibility to manage detections efficiently. Users can choose to save, ignore, or cancel a detected face based on their preferences. The system ensures accurate recognition and seamless interaction. Designed for reliability, it provides an intuitive interface for handling facial data effortlessly.

## 🚀 Features

- **Real-time Face Detection** using OpenCV 📷

- **Save Faces** to recognize them later 🏷️

- **Ignore Faces** to prevent them from being recognized again 🚫

- **Beautiful GUI** with an easy-to-use interface 🎨

- **Live Bounding Box** around detected faces 🟩

- **Smooth Performance** with multithreading ⚡

## 🖼️ User Interface

- The main window has three buttons:

  - **Start Detection** 🟢
  - **Stop Detection** 🟠
  - **Exit** 🔴

- When saving a face, a popup shows:
  - The detected **face with a bounding box** 🟩
  - Buttons for **Save**, **Ignore**, and **Cancel**

## 🔧 How to Setup

## 🛠️ How to Set Up This Project

This guide will help you set up the project's environment seamlessly.

**<u>1. Install Python</u> 🐍**

If you haven't installed Python yet, visit the official download page: [Python Download Guide](https://wiki.python.org/moin/BeginnersGuide/Download) and follow the instructions for your operating system (Windows, macOS, or Linux).

**<u>2. Create a Virtual Environment</u>**

1. Creating a virtual environment:

   - In the terminal, run this command:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - To activate the virtual environment, use:

   ```bash
   .\venv\Scripts\activate
   ```

**3. Clone the Repository 📥**

1. Open your Git client or terminal.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command, replacing `<repository_url>` with the actual URL of the project's repository:

```bash
git clone <repository_url>
```

**4. Install CMake in your computer**

- You can install CMake from [here](https://cmake.org/download/)

**5. Install required Dependencies 📦**

1. Open terminal/cmd.
2. Navigate to repo directory
3. Run the following command to install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

**6. Run the Python Script**

- After installing the required dependencies, run the following command to run the python script:

```bash
python main.py
```

## How does it work?

- The app **captures frames** from the webcam.
- It **detects faces** and encodes them.
- If a face is **unknown**, it asks you whether to **save or ignore** it.
- Recognized faces get a **bounding box and label**.

## ❤️ Credits

Built with **Python**, **OpenCV**, and **Tkinter** by an amazing developer! 🚀
