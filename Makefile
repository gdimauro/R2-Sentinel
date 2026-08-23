# =============================================================================
# R2-Sentinel — punto di ingresso unico della piattaforma software.
#
# Se un comando non e' qui dentro, non e' riproducibile: e' una cosa che sa
# fare solo chi l'ha scritta. `make help` elenca tutto.
# =============================================================================

SHELL := /bin/bash
ROOT  := $(shell git rev-parse --show-toplevel 2>/dev/null || pwd)
VENV  := $(ROOT)/.venv
PY    := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PYTEST:= $(if $(wildcard $(VENV)/bin/pytest),$(VENV)/bin/pytest,python3 -m pytest)
WS    := $(ROOT)/software/ros2_ws
BASE  ?= origin/main
HEAD  ?= HEAD

.DEFAULT_GOAL := help
.PHONY: help bootstrap check check-diff test test-bench fatto fatto-list coverage \
        build firmware mqtt-docs models models-hash history-scan lfs \
        verify-clean docker-shell docker-ci lint clean distclean

help: ## Elenca i comandi disponibili
	@echo "R2-Sentinel — comandi di piattaforma"
	@echo
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "Primo giorno:   ./scripts/bootstrap.sh"
	@echo "Prima di una PR: make check && make test"

# --- ambiente ---------------------------------------------------------------

bootstrap: ## Da git clone a workspace compilato (un solo comando)
	@./scripts/bootstrap.sh

lfs: ## Gate 0: verifica Git LFS, con prova end-to-end
	@./scripts/ci/check_lfs.sh --prove

# --- controlli --------------------------------------------------------------

check: ## Igiene su tutto il worktree + schema MQTT (quello che gira in CI)
	@$(PY) scripts/ci/check_hygiene.py --worktree
	@$(PY) scripts/ci/check_mqtt_topics.py
	@$(PY) scripts/gen/gen_mqtt_docs.py --check
	@./scripts/ci/check_lfs.sh

check-diff: ## Igiene sul solo diff verso BASE (default origin/main)
	@$(PY) scripts/ci/check_hygiene.py --diff $(BASE) $(HEAD)
	@$(PY) scripts/ci/check_decision_log.py --diff $(BASE) $(HEAD)
	@$(PY) scripts/ci/check_compliance_gate.py --diff $(BASE) $(HEAD)

history-scan: ## 0 binari >5 MB e 0 materiale privato nella history
	@./scripts/ci/check_history_binaries.sh 5
	@./scripts/ci/check_history_private.sh

lint: ## Lint python della piattaforma
	@$(if $(wildcard $(VENV)/bin/ruff),$(VENV)/bin/ruff check scripts tests,\
	  echo "ruff non installato: esegui ./scripts/bootstrap.sh --only python")

# --- test -------------------------------------------------------------------

test: ## Test che NON richiedono hardware (girano ovunque)
	@$(PYTEST) tests/ci tests/bench -q

test-bench: ## Test da banco (richiede hardware collegato e dichiarato)
	@R2S_BENCH=1 $(PYTEST) tests -q

fatto: ## Esegue i criteri di FATTO eseguibili (ROLE=<ruolo> per filtrare)
	@./scripts/fatto.sh $(ROLE)

fatto-list: ## Elenco dei criteri di FATTO con il loro stato
	@./scripts/fatto.sh --list

coverage: ## Quanti criteri di FATTO hanno un comando, per ruolo
	@./scripts/fatto.sh --coverage

# --- build ------------------------------------------------------------------

build: ## Compila il workspace ROS 2
	@set -e; source /opt/ros/jazzy/setup.bash; cd $(WS); \
	 colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo

firmware: ## Compila il firmware ESP32-S3 da zero
	@./scripts/ci/build_firmware.sh

# --- artefatti generati -----------------------------------------------------

mqtt-docs: ## Rigenera docs/interfaces/MQTT.md dallo schema dei topic
	@$(PY) scripts/gen/gen_mqtt_docs.py

models: ## Scarica e verifica i pesi dichiarati in models/MANIFEST.yaml
	@$(PY) scripts/models/fetch_models.py

models-hash: ## Calcola lo sha256 di un file: make models-hash FILE=percorso
	@$(PY) scripts/models/fetch_models.py --hash $(FILE)

# --- riproducibilita' -------------------------------------------------------

verify-clean: ## Bootstrap su container vergine, 2 volte (criterio di FATTO)
	@./scripts/verify_clean_bootstrap.sh --runs 2

docker-shell: ## Shell in una Ubuntu 24.04 vergine con il repo montato
	@docker build -q -f docker/ubuntu2404-clean.Dockerfile -t r2s-clean:latest . >/dev/null
	@docker run --rm -it -v "$(ROOT):/home/dev/R2-Sentinel" r2s-clean:latest bash

docker-ci: ## Costruisce l'immagine di CI (Ubuntu 24.04 + ROS 2 Jazzy)
	@docker build -f docker/ci.Dockerfile -t r2s-ci:jazzy .

# --- pulizia ----------------------------------------------------------------

clean: ## Rimuove gli artefatti di build
	@rm -rf $(WS)/build $(WS)/install $(WS)/log firmware/esp32/build reports artifacts
	@find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@echo "pulito"

distclean: clean ## Rimuove anche il venv di piattaforma
	@rm -rf $(VENV)
	@echo "rimosso .venv (rilancia ./scripts/bootstrap.sh)"
