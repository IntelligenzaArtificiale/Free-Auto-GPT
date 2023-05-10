#!/bin/bash

echo "What program do you want to use?"
echo "1- AutoGPT"
echo "2- BabyAGI"
echo "3- Camel"
echo "4- MetaPrompt"
echo "5- Others"
echo

read -p "Write the number >>> " user_input

case $user_input in
    1)
        echo "Starting AutoGPT..."
        python "$(dirname "$0")/AUTOGPT.py"
        ;;
    2)
        echo "Starting BabyAGI..."
        python "$(dirname "$0")/BABYAGI.py"
        ;;
    3)
        echo "Starting Camel..."
        python "$(dirname "$0")/Camel.py"
        ;;
    4)
        echo "Starting MetaPrompt..."
        python "$(dirname "$0")/MetaPrompt.py"
        ;;
    5)
        echo "Choose other agents"
        echo
        echo "What custom agents do you want to use?"
        echo "1- csvAgent"
        echo "2- customAgent"
        echo "3- pythonAgent"
        echo

        read -p "Write the number >>> " user_input2

        case $user_input2 in
            1)
                echo "Starting csvAgent..."
                echo "Current directory: $(pwd)"
                echo "Python file path: $(dirname "$0")/OtherAgent/csvAgent.py"
                cd OtherAgent
                python csvAgent.py
                ;;
            2)
                echo "Starting customAgent..."
                echo "Current directory: $(pwd)"
                echo "Python file path: $(dirname "$0")/OtherAgent/customAgent.py"
                cd OtherAgent
                python customAgent.py
                ;;
            3)
                echo "Starting pythonAgent..."
                echo "Current directory: $(pwd)"
                echo "Python file path: $(dirname "$0")/OtherAgent/pythonAgent.py"
                cd OtherAgent
                python pythonAgent.py
                ;;
            *)
                echo "Invalid input2"
                ;;
        esac
        ;;
    *)
        echo "Invalid input"
        ;;
esac
