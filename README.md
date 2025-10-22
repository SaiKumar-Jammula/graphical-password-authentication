# 🖼️ Graphical Password Authentication Using Cued Click Points

## 📘 Overview
This project implements a **Graphical Password Authentication System** using **Cued Click Points (CCP)** — a secure and user-friendly alternative to traditional text-based passwords.  
Users register with basic credentials and then select **one click-point on each of five images** to create their graphical password. During login, they must click on the same cued points to authenticate successfully.  
After successful authentication, users can **lock and unlock files or folders**, making this system both practical and secure.

---

## 🧠 Objective
Traditional text passwords are easy to forget and often insecure.  
This project enhances security and usability by using **visual memory** instead of text recall, helping users remember passwords more naturally while resisting brute-force or dictionary attacks.

---

## ⚙️ Features
- **User Registration** with email and password  
- **Graphical Password Setup** using 5 user-selected images  
- **Cued Click Points Authentication** with visual feedback  
- **File/Folder Locking and Unlocking** after successful login  
- **Full-Screen GUI** with modern, centered layout  
- **Secure Local Data Storage** using JSON  
- **Tolerance-based Matching** for human clicking variations  

---

## 🏗️ System Architecture
The application is divided into several modules:

1. **User Registration Module** – Collects user credentials and stores them securely.  
2. **Graphical Password Setup Module** – Allows the user to set cued click-points on images.  
3. **Authentication Module** – Validates user clicks during login.  
4. **File/Folder Access Module** – Enables secure locking/unlocking operations.  
5. **Data Management Module** – Handles reading/writing of JSON files.  

---

## 🖥️ Technologies Used

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.8+ |
| **GUI Library** | Tkinter |
| **Image Processing** | Pillow (PIL) |
| **Data Storage** | JSON |
| **File Operations** | os, shutil, subprocess |
| **Serialization** | pickle |
| **OS Compatibility** | Windows / Linux (Ubuntu recommended) |

---

## 💻 Hardware Requirements
- Processor: Intel i3 or above  
- RAM: Minimum 4 GB  
- Disk Space: 100 MB  
- Display: 1366×768 or higher  
- Input: Mouse and Keyboard  

---

## 🧩 How It Works

### 🔹 Registration
- User enters **email and password**.
- User selects **5 images**.
- For each image, the user clicks a point — stored as coordinates in a JSON file.

### 🔹 Login
- User enters email and password.
- The same images are displayed one by one.
- User clicks the same cued points.
- If all clicks match (within tolerance), access is granted.

### 🔹 File/Folder Protection
- After successful login, users can **lock or unlock** predefined files or folders.
- Locking hides the resource using OS attributes until re-authenticated.

---

## 📂 Project Structure
```
📁 Graphical_Password_Auth/
│
├── main.py                   # Main Python script
├── password_data.json         # Stores cued click-point data
├── user_data.json             # Stores user credentials
├── images/                    # Folder containing user-selected images
├── README.md                  # Project documentation
└── lock.PNG                   # Lock icon used in GUI
```

---

## 🧪 Testing Performed
- **Unit Testing:** Verified each module independently.  
- **Integration Testing:** Ensured smooth flow between registration, login, and file access.  
- **System Testing:** Validated the complete workflow.  
- **Usability Testing:** Confirmed clarity and ease of GUI navigation.  
- **Security Testing:** Checked resistance to unauthorized access.  
- **Performance Testing:** Ensured stable performance with multiple user entries.  

---

## 🧾 Results
- Users could easily remember graphical passwords.
- Authentication accuracy improved due to visual cues.
- The system successfully secured local files/folders post-login.
- Compared to text passwords, CCP reduced memorability errors and improved usability.

---

## 🚀 Future Enhancements
- Implement password recovery via email or SMS.
- Introduce **multi-user support**.
- Add **AES encryption** for stored password data.
- Integrate with **biometric or OTP-based secondary authentication**.

---

## 🧑‍💻 Author
**Name:** JAMMULA SAI KUMAR  
**ID:** 24000I1003  
**Program:** M.Sc. (Computer Science), Kakatiya University  
**Guide:** Dr. D. RAMESH, Assistant Professor  

---

## 📜 License
This project is developed as part of the **M.Sc. Dissertation Work (2023–2025)** and is intended for **academic and research purposes** only.
