# Certificates on Blockchain

## Introduction
The **Certificates on Blockchain** project provides a decentralized, immutable, and secure system for verifying academic and professional certificates using blockchain technology. This eliminates the risks of forgery and streamlines the certificate validation process for institutions and employers.

## License
This project is open-source under the **MIT License**.

## Research Paper
This project is based on the research paper **[Blockchain-Based Certificate Verification System: A Decentralized Approach](https://link.springer.com/chapter/10.1007/978-981-97-3601-0_367)**, which explores how blockchain can be utilized for secure and transparent certificate verification.

## Features
- **Decentralized Verification**: Uses blockchain to store and verify certificates.
- **Immutable Records**: Certificates are tamper-proof once added to the blockchain.
- **QR Code Authentication**: Each certificate has a QR code linked to its blockchain record.
- **User Roles**: 
  - **Admin**: Issues and revokes certificates.
  - **Student**: Requests and views their certificates.
  - **Verifier**: Validates certificate authenticity.
- **CSV Export**: Admins can export student records and certificates to CSV.
- **Email Notifications**: Sends automated emails when a certificate is issued.
- **Django Admin Panel**: Manage students, courses, and certificates via an intuitive interface.

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: React.js (or Django templates if applicable)
- **Blockchain**: Ethereum/Solidity (or Hyperledger, depending on implementation)
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT / OAuth2
- **QR Code Generation**: `qrcode` Python library
- **Email Service**: Mailjet / SMTP

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Node.js (if frontend uses React)
- PostgreSQL / SQLite
- Metamask / Ganache (for blockchain testing)

### Backend Setup
```sh
# Clone the repository
git clone https://github.com/your-repo/certificatesonblockchain.git
cd certificatesonblockchain

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### Frontend Setup (If applicable)
```sh
cd frontend  # Navigate to the frontend directory
npm install  # Install dependencies
npm start    # Start the frontend development server
```

## Usage
- **Admin** logs into the Django admin panel to issue or revoke certificates.
- **Students** can log in to request and view their certificates.
- **Verifiers** can scan the QR code or enter the certificate ID to validate authenticity.

## API Endpoints (Example)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/certificates/` | GET | Get all certificates |
| `/api/certificates/<id>/` | GET | Get certificate details |
| `/api/certificates/issue/` | POST | Issue a new certificate |
| `/api/certificates/verify/` | POST | Verify a certificate |

## Contribution Guidelines
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch (`feature/new-feature` or `bugfix/fix-issue`).
3. Commit your changes with meaningful messages.
4. Push to your fork and submit a pull request.

## Contributors
- **Lovnish Verma** [(@lovnishVerma)](https://github.com/lovnishVerma)
- **Anita Budhiraja**
- **Dr. Sarwan Singh** [(@sarwansingh)](https://github.com/sarwansingh)

## License
This project is licensed under the **MIT License**.

---
Feel free to suggest any improvements or report issues in the repository!
