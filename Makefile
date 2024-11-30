# Atur PYTHONPATH ke direktori root proyek
PYTHONPATH=$(shell pwd)

# Daftar service dan path ke file main.py
API_GATEWAY=internal/services/api_gateway/main.py
AUTH_SERVICE=internal/services/auth_service/main.py
EMAIL_SERVICE=internal/services/email_service/main.py
SALDO_SERVICE=internal/services/saldo_service/main.py
TOPUP_SERVICE=internal/services/topup_service/main.py
TRANSFER_SERVICE=internal/services/tranfer_service/main.py
USER_SERVICE=internal/services/user_service/main.py
WITHDRAW_SERVICE=internal/services/withdraw_service/main.py

# Default target untuk menampilkan opsi
.PHONY: help
help:
	@echo "Usage: make [service-name]"
	@echo "Available services:"
	@echo "  api-gateway"
	@echo "  auth-service"
	@echo "  email-service"
	@echo "  saldo-service"
	@echo "  topup-service"
	@echo "  transfer-service"
	@echo "  user-service"
	@echo "  withdraw-service"

# Target untuk masing-masing service
.PHONY: api-gateway
api-gateway:
	PYTHONPATH=$(PYTHONPATH) python $(API_GATEWAY)

.PHONY: auth-service
auth-service:
	PYTHONPATH=$(PYTHONPATH) python $(AUTH_SERVICE)

.PHONY: email-service
email-service:
	PYTHONPATH=$(PYTHONPATH) python $(EMAIL_SERVICE)

.PHONY: saldo-service
saldo-service:
	PYTHONPATH=$(PYTHONPATH) python $(SALDO_SERVICE)

.PHONY: topup-service
topup-service:
	PYTHONPATH=$(PYTHONPATH) python $(TOPUP_SERVICE)

.PHONY: transfer-service
transfer-service:
	PYTHONPATH=$(PYTHONPATH) python $(TRANSFER_SERVICE)

.PHONY: user-service
user-service:
	PYTHONPATH=$(PYTHONPATH) python $(USER_SERVICE)

.PHONY: withdraw-service
withdraw-service:
	PYTHONPATH=$(PYTHONPATH) python $(WITHDRAW_SERVICE)
