@echo off
:: 한글 깨짐 방지를 위해 UTF-8 코드로 변경
chcp 65001 > nul

echo ==========================================
echo   News Curation Bot 자동 실행 삭제 도구
echo ==========================================
echo.
echo 이 스크립트는 윈도우 작업 스케줄러에 등록된 
echo 'NewsCurationMacroBot' 작업을 삭제합니다.
echo.
schtasks /delete /tn "NewsCurationMacroBot" /f
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [성공] 자동 실행 작업이 삭제되었습니다.
) else (
    echo.
    echo [실패] 관리자 권한으로 실행했는지 확인해 주세요.
)
echo.
pause
