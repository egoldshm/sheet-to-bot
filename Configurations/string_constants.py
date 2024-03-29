COMMAND_NOT_FOUND_MESSAGE = "לא הבנתי 🤷‍♂️"

RETURN_MENU_MESSAGE = "חזור לתפריט הראשי 🔙"
RETURN_ONE_ASK = "חזור אחורה 🔙"

RETURN_MESSAGE = "חזרתי 🔙"

IGNORE_WORDS = ["הרב", "מר", "פרופ'", "גב'", """ד"ר""", "גברת"]

WHAT_WE_FOUND_MESSAGE = "*הנה כל מה שמצאנו שמתאים לחיפוש שלך: 🔍*\n "

LIST_OF_ITEMS_FOUND_SIGN = "🔵"
SEND_MESSAGE_TO_ALL = "שלח לכולם:\n"
SEND_TO_USER = "שלח הודעה:\n"
MENU_LIST = ("מה אתה יודע לעשות?", "מה יש בבוט?", "רשימת פקודות", "תפריט")
RESET_MESSAGE = "/reset"

DONE_FORM_MESSAGE = "סיימתי 👍"
RECEIVED_MESSAGE_FORM = "קיבלתי את ההודעה 👍📢 מוזמן לסיים על ידי לחיצה על הכפתור למטה - או לשלוח לי עוד הודעות 😉"

FORWARD_TO_ALL = "/forwardToAll"
SEND_ONLY_TO_ME = "שלח לי 😊"
CANCEL = "ביטול ❌"
RESPONSE_TO_FORWARD_TO_ALL = "אחלה, עכשיו שלח את ההודעות. ולסיום לחץ על 'שלח לי' או על 'שלח לכולם'"
ADMIN_GET_ALL_USERS = "/allUsers"
FREE_SEARCH_IN_DATA = "חח:\n"

ADMIN_MENU_COMMAND = ("/admin", "admin", "מנהלים", "תפריט ניהול")
ADMIN_MENU = """*מה אתה בתור מנהל יכול לעשות?*
1. *לשלוח הודעה לכולם* - תשלח "{}" (בלי גרשיים, כמובן) ושורה מתחת תכתוב את ההודעה שאתה רוצה לשלוח לכולם. זה ישלח לכולם.
2. *להעביר הודעה לכולם* - תכתוב פשוט "{}", ותפעל לפי ההוראות.
3. *לשלוח הודעה פרטית* - תכתוב פשוט "{}", ואז שורה מתחת את הID של המשתמש שאתה רוצה לשלוח לו, ושורה מתחת את הטקסט.
4. *לאפס את התפריט* - תשלח "{}", וזה פשוט יאפס את התפריט. יש לעשות את זה אחרי עדכון של התוכן בבוט.
5. *לקבל מידע על הודעה* - תשלח הודעה שהיא לא טקסט. ותקבל את המידע המלא עליה.
6. *לקבל רשימה מלאה של המשתמשים שבבוט* - תכתוב {}""".format(SEND_MESSAGE_TO_ALL.strip(), FORWARD_TO_ALL, SEND_TO_USER.strip(),
                                            RESET_MESSAGE,ADMIN_GET_ALL_USERS)

TEXT_TO_CHANNEL_REPORT = """<a href="tg://user?id={}"><u>משתמש 💬:</u></a>
{}
<u>מספר הודעה 🔢:</u>
<code>{}</code>
<u>הודעה 💬:</u>
<b>{}</b>
<u>תשובה 🗨:</u>
{}
<u>צומת 🌴:</u>
{}"""

ERROR_MESSAGE_TO_CHANNEL = """#ERROR
(Exception in messageHandler)
Explanation: {}
User: {}
Text: {}
"""








