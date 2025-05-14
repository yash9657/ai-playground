import pytesseract
import pyautogui
from dotenv import load_dotenv
import os
from pynput import keyboard
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_answer_from_openai(question_and_answers):
    print(question_and_answers)
    # Adding explicit instructions to the LLM
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant specialized in answering multiple choice questions. Please respond with just the number either 1,2,3 or 4 out of the list of options provided."
        },
        {
            "role": "user",
            "content": question_and_answers
        },
    ]

    try:
        response = client.chat.completions.create(model="gpt-4.1", messages=conversation)
        reply = response.choices[0].message.content
        return int(reply)
    except ValueError:
        print(f"Unexpected reply: {reply}")
        return None
    except:
        print("Something went wrong.")
        return None

def click_kahoot_answer(answer_number):
    """
    Simulate a mouse click on the Kahoot answer button corresponding to the answer_number (1-4).
    """
    # Map answer_number to the region coordinates (same as in extract_kahoot_question_and_options)
    answer_regions = {
        1: { "top_left": (20, 680), "bottom_right": (727, 795) },
        2: { "top_left": (742, 680), "bottom_right": (1450, 795) },
        3: { "top_left": (20, 817), "bottom_right": (727, 932) },
        4: { "top_left": (742, 817), "bottom_right": (1450, 932) }
    }
    if answer_number not in answer_regions:
        print(f"Invalid answer number: {answer_number}")
        return

    region = answer_regions[answer_number]
    x1, y1 = region["top_left"]
    x2, y2 = region["bottom_right"]

    # Calculate the center of the answer button
    center_x = x1 + (x2 - x1) // 2
    center_y = y1 + (y2 - y1) // 2

    # Move the mouse to the center and click
    pyautogui.moveTo(center_x, center_y, duration=0.2)
    pyautogui.click()
    print(f"Clicked answer {answer_number} at ({center_x}, {center_y})")

def extract_kahoot_question_and_options():
    question_and_answers = {
        0: { "top_left": (0, 158), "bottom_right": (1468, 353) },
        1: { "top_left": (20, 680), "bottom_right": (727, 795) },
        2: { "top_left": (742, 680), "bottom_right": (1450, 795) },
        3: { "top_left": (20, 817), "bottom_right": (727, 932) },
        4: { "top_left": (742, 817), "bottom_right": (1450, 932) }
    }
    res = ""
    for element in question_and_answers:
        coordinates = question_and_answers[element]
        x1, y1 = coordinates["top_left"]
        x2, y2 = coordinates["bottom_right"]

        width = x2 - x1
        height = y2 - y1

        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        screenshot_text = pytesseract.image_to_string(screenshot)
        if not screenshot_text.strip():
            print("No text detected.")
            continue
        if element == 0:
            res += f"Question: {screenshot_text}\n"
            # print(f"Question: {screenshot_text}")
        else:
            idx = screenshot_text.find(" ")
            if idx != -1:
                new_text = screenshot_text[idx+1:]
            else:
                new_text = ""
            res += f"Answer {element}: {new_text}\n"
            # print(f"Answer {element}: {new_text}")
    answer = get_answer_from_openai(res)
    click_kahoot_answer(answer)

def on_activate():
    print("Hotkey pressed! Extracting Kahoot question and options...")
    extract_kahoot_question_and_options()

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<space>'),
    on_activate
)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()