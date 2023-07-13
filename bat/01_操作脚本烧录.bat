REM 2023-07-13
REM 操作脚本烧录
@echo off & setlocal enabledelayedexpansion
chcp 65001 > NUL

REM 调用获取串口列表
call :__get_serialport_lists
goto :__input_port_num

REM 获取串口列表
:__get_serialport_lists
echo ----------------------------
set "portList="
set "existCom="
set "comMsg="

for /f "tokens=1,2*" %%A in ('mode ^| findstr "COM"') do (
    for /f "tokens=2 delims=: " %%B in ("%%C") do (set "portList=!portList! %%B")
)

if defined portList (
    set "comMsg=1.查询到目前的串口列表为"
    set "existCom=1"
    set "portList=!portList:~1!"
) else (
    set "comMsg=错误1.请检查一下串口是否有插入!"
)

if "%existCom%"=="1" (
    echo %comMsg%: %portList%
    goto :__input_port_num
) else (
    echo %comMsg%
    goto :eof
)

REM 烧录
:__input_port_num
echo ----------------------------
set /p com="请输入烧录的串口号:"
REM echo %com% 
echo ----------------------------
goto brun


REM 结束脚本
:end
endlocal
pause
exit /b 0

:brun
REM open tools and use %com% to brun
echo "brun"
echo COM%com%

