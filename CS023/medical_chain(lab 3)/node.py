import socket
import threading
import json
import requests

class Node:
    def __init__(self, role, node_name, host='127.0.0.1', port=5001):
        self.role = role
        self.node_name = node_name
        self.host = host
        self.port = port
        self.peers = []  # List of connected nodes

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[{self.node_name} Node] Running at {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        data = client.recv(1024).decode()
        if data:
            print(f"[{self.node_name} Received]: {data}")
            self.broadcast(data)
        client.close()

    def broadcast(self, message):
        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(peer)
                s.sendall(message.encode())
                s.close()
            except:
                pass

    def connect_to_peer(self, peer_host, peer_port):
        self.peers.append((peer_host, peer_port))

    def send_data_to_server(self, endpoint, data):
        url = f"http://127.0.0.1:5000/{endpoint}"
        response = requests.post(url, json=data)
        print(f"[{self.node_name} API Response]:", response.json())

    def view_patient_details(self, patient_id):
        url = "http://127.0.0.1:5000/get_chain"
        response = requests.get(url)
        chain = response.json()

        patient_records = [block for block in chain if block["patient_id"] == patient_id]
        
        if patient_records:
            print("\n🔹 Patient Medical Records:")
            for record in patient_records:
                print(f"- Action: {record['action']}, Doctor: {record['doctor_id']}, Details: {record.get('test_results') or record.get('prescription')}")
        else:
            print("\n⚠️ No records found for this patient.")

if __name__ == "__main__":
    print("Select Role: ")
    print("1. Doctor")
    print("2. Pharmacy")
    print("3. User (Patient)")
    
    role_choice = input("Enter your choice: ")

    if role_choice == "1":
        role = "Doctor"
    elif role_choice == "2":
        role = "Pharmacy"
    elif role_choice == "3":
        role = "User"
    else:
        print("Invalid choice. Exiting.")
        exit()

    port = int(input("Enter port number for this node (5001-5003): "))
    node = Node(role, role, port=port)
    threading.Thread(target=node.start_server).start()

    while True:
        print("\n1. Add New Patient (Doctor Only)")
        print("2. Add Test Result (Doctor Only)")
        print("3. Add Prescription (Doctor Only)")
        print("4. Retrieve Prescription (Pharmacy Only)")
        print("5. View Patient Details (User Only)")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if role == "Doctor":
            if choice == "1":
                patient_id = input("Enter Patient ID: ")
                doctor_id = input("Enter Doctor ID: ")
                node.send_data_to_server("new_patient", {"patient_id": patient_id, "doctor_id": doctor_id})

            elif choice == "2":
                patient_id = input("Enter Patient ID: ")
                doctor_id = input("Enter Doctor ID: ")
                test_results = input("Enter Test Results: ")
                node.send_data_to_server("add_test_result", {"patient_id": patient_id, "doctor_id": doctor_id, "test_results": test_results})

            elif choice == "3":
                patient_id = input("Enter Patient ID: ")
                doctor_id = input("Enter Doctor ID: ")
                prescription = input("Enter Prescription: ")
                node.send_data_to_server("add_prescription", {"patient_id": patient_id, "doctor_id": doctor_id, "prescription": prescription})

        elif role == "Pharmacy":
            if choice == "4":
                patient_id = input("Enter Patient ID to retrieve prescription: ")
                node.view_patient_details(patient_id)

        elif role == "User":
            if choice == "5":
                patient_id = input("Enter your Patient ID: ")
                node.view_patient_details(patient_id)

        if choice == "6":
            break
