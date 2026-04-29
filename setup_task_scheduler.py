import os
import subprocess
from pathlib import Path

def setup_task():
    print("=== 뉴스 큐레이션 봇 자동 실행 설정 ===")
    
    # run_bot.bat 경로 확인
    bot_dir = Path(__file__).resolve().parent
    bat_path = bot_dir / "run_bot.bat"
    
    if not bat_path.exists():
        print(f"오류: {bat_path} 파일을 찾을 수 없습니다.")
        return
        
    task_name = "NewsCurationMacroBot"
    
    # PowerShell을 사용하여 작업 등록 (공백 및 특수 문자 경로 처리)
    # 경로 내에 홑따옴표(')가 있을 경우를 대비해 이스케이프 처리
    bat_path_esc = str(bat_path).replace("'", "''")
    bot_dir_esc = str(bot_dir).replace("'", "''")
    
    ps_command = f"""
    $action = New-ScheduledTaskAction -Execute '{bat_path_esc}' -WorkingDirectory '{bot_dir_esc}';
    $trigger = New-ScheduledTaskTrigger -AtLogOn;
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries;
    Register-ScheduledTask -TaskName '{task_name}' -Action $action -Trigger $trigger -Settings $settings -Force
    """

    
    # PowerShell 전체 경로 사용 (환경 변수 문제 방지)
    ps_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    command = [ps_path, "-NoProfile", "-Command", ps_command]

    
    print(f"작업 스케줄러에 등록 시도 중: {task_name}")
    print("주의: 이 작업은 '관리자 권한'이 필요할 수 있습니다.")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("작업 스케줄러 등록 성공!")
    except subprocess.CalledProcessError as e:
        print("\n[오류] 작업 스케줄러 등록에 실패했습니다.")
        print("이 스크립트를 '관리자 권한으로 실행(Run as Administrator)' 하거나,")
        print("터미널을 관리자 권한으로 열어 실행해 주세요.")
        print(f"상세 오류: {e.stderr}")

if __name__ == "__main__":
    setup_task()

