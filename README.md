# 🚑 Emergency Department Simulation Project

This repository contains a **discrete-event simulation model** of an emergency department, developed in **Python** using the `simpy` library. The goal of the project is to simulate and analyze patient flows, resource allocation, and treatment times to optimize the performance of the emergency room under various scenarios.

---

## 📋 Project Structure

The repository is structured as follows:

```
├── main.py          # Main simulation script
├── requirements.txt # Python dependencies
├── results/         # Folder to store simulation results
└── README.md        # Project documentation
```

---

## ⚙️ Installation and Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/Pache43/Emergency-Room-ModelSim.git
   cd Emergency-Room-ModelSim
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulation:

   ```bash
   python main.py
   ```

---

## 🧩 Key Features

- **Patient Flow Simulation:**  
  Simulates patient arrivals and treatment processes based on different patient types.

- **Randomized Treatment Times:**  
  Uses triangular distributions to model realistic treatment durations.

- **Resource Management:**  
  Manages limited resources such as doctors, X-ray machines, and plaster rooms using `simpy`.

- **Statistical Analysis:**  
  Calculates key metrics like average treatment time, queue lengths, and standard deviation.

---

## 📊 Simulation Overview

The simulation models four types of patients with different treatment paths:

| Patient Type | Description                | Treatment Steps                       |
|--------------|----------------------------|---------------------------------------|
| Type 1       | Requires X-ray              | Registration → CW → X-ray → CW        |
| Type 2       | Requires plaster treatment  | Registration → CW → Plaster           |
| Type 3       | Requires multiple treatments| Registration → CW → X-ray → Plaster → X-ray → CW |
| Type 4       | Minor issues, no treatment  | Registration → Exit                   |

---

## 📈 Results and Analysis

The simulation provides the following key outputs:

- **Overall Average Treatment Time**
- **Queue Lengths for Resources**
- **Standard Deviation of Treatment Times**

Results are saved as a CSV file in the `results/` directory.

---

## 🛠️ Technologies Used

- **Python 3.10+**  
- **SimPy** (for discrete-event simulation)  
- **CSV** (for data export)  

---

## 📖 Tasks Overview

The project is divided into the following tasks:

1. **Task 1:** Patient registration and queue management.  
2. **Task 2:** Queue limitations.  
3. **Task 3:** Priority handling and resource allocation.  

---

## 📚 Further Reading

- [SimPy Documentation](https://simpy.readthedocs.io/en/latest/)  
- [Python Official Documentation](https://docs.python.org/3/)

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. Contributions are welcome!

---