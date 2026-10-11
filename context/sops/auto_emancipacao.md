# 📋 SOP: Monitoramento de Escopo e Auto-Emancipação

> **Código:** `SOP-GOV-001`  
> **Responsável:** `arquiteto_agent.md` | **Decisor:** `<Autor / Decisor do Projeto>`  

---

## 1. Objetivo
Evitar a degradação de performance e a sobrecarga de contexto do orquestrador através da segregação autônoma de módulos de alta densidade.

## 2. Limiares de Alerta e Críticos
* **Aviso de Densidade:** 30 arquivos em um único submódulo.
* **Gatilho de Emancipação:** 40 arquivos em um único submódulo.

## 3. Fluxo de Emancipação
1. Executar auditoria de densidade:
   ```bash
   uv run python3 tools/scope_monitor.py
   ```
2. Ao detectar estado crítico, emitir RFC:
   ```bash
   uv run python3 tools/scope_monitor.py --auto-rfc
   ```
3. Submeter a proposta gerada em `context/memory/propostas/` à aprovação do decisor.
4. Após aprovação, executar a separação para repositório independente via:
   ```bash
   uv run python3 tools/autopilot.py emancipate --module "nome_do_modulo"
   ```
