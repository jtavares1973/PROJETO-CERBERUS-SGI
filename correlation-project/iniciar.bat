@echo off
REM ════════════════════════════════════════════════════════════════
REM INICIO RAPIDO - Validacao com IA (Windows)
REM ════════════════════════════════════════════════════════════════

echo.
echo ════════════════════════════════════════════════════════════════
echo VALIDACAO COM IA - INICIO RAPIDO
echo ════════════════════════════════════════════════════════════════
echo.

REM Verifica se esta no diretorio correto
if not exist "scripts\validar_com_ia.py" (
    echo ❌ ERRO: Execute este script da pasta correlation-project\
    pause
    exit /b 1
)

REM Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python nao encontrado
    pause
    exit /b 1
)

REM Verifica Ollama
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Ollama nao instalado
    echo    Instale em: https://ollama.ai
    pause
    exit /b 1
)

REM Verifica modelo
ollama list | findstr "qwen2.5-ptbr:7b" >nul
if %errorlevel% neq 0 (
    echo ⚠️  Modelo qwen2.5-ptbr:7b nao encontrado
    echo.
    set /p resposta="Deseja instalar agora? (s/n): "
    if /i "%resposta%"=="s" (
        echo Instalando modelo (4.7GB)...
        ollama pull qwen2.5-ptbr:7b
    ) else (
        echo ❌ Modelo necessario para continuar
        pause
        exit /b 1
    )
)

echo.
echo ✅ Pre-requisitos OK!
echo.
echo ════════════════════════════════════════════════════════════════
echo ABRINDO 2 JANELAS...
echo ════════════════════════════════════════════════════════════════
echo.
echo   Janela 1: Validacao com IA
echo   Janela 2: Monitor de progresso
echo.
echo   DICA: Execute 'python scripts\configurar_validacao.py'
echo         para ajustar modelo, temperatura, etc.
echo.
timeout /t 3 >nul

REM Abre Terminal 1: Validacao
start "Validacao IA" cmd /k "python scripts\validar_com_ia.py"

REM Aguarda 3 segundos
timeout /t 3 >nul

REM Abre Terminal 2: Monitor
start "Monitor Progresso" cmd /k "python scripts\monitor_progresso.py"

echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ JANELAS ABERTAS!
echo ════════════════════════════════════════════════════════════════
echo.
echo Feche esta janela. As outras continuarao rodando.
echo.
pause
