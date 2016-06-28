UI_Path=UI

echo "Generating UIs...\n"
echo "Generating MainUI"
pyuic4 -o $UI_Path/MainUI/MainUI.py $UI_Path/MainUI/MainUI.ui

echo "\nStarting Interface\n"
python GUI.py
