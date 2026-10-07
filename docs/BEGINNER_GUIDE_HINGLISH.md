# Onboarding Copilot: bilkul basic se

## 1. Hum yeh project kyun bana rahe hain?

Maan lo ABC Company ne employees ki attendance manage karne ke liye ek online software kharida.
Kharidne ke baad bhi uska account banana, employees ki details add karna, settings configure karna,
testing karna aur HR team ko training dena baaki hai.

Customer ko product sahi tarah use karne ke liye ready karne ka process CUSTOMER ONBOARDING hai.
SaaS (Software as a Service) ka matlab internet ke through milne wala software hai.
Provider uski hosting, updates aur maintenance handle karta hai.

Hamara tracker attendance software khud nahi hai.
Yeh us software ko customer ke liye ready karne wale KAAM track karta hai.

Agar aise 8 customers hon, toh emails aur memory ke bharose sab follow-ups yaad rakhna mushkil hai.
Tracker batata hai: kis customer ke liye kya karna hai, kaun karega, kab tak karega aur kitna hua hai.

## 2. Iska use kaun karega?

Customer success executive: customer ke setup aur training ka follow-up.
Program coordinator: tasks aur deadlines organize karna.
Implementation team: setup ka pending kaam dekhna.

Publive ki internship mein onboarding, task coordination, customer communication aur follow-ups hain.
Isliye yeh portfolio project us role ki practical thinking practice karwata hai.
Yeh Publive ka actual internal software ya uske product ka integration nahi hai.

## 3. Basic version abhi kya karti hai?

- Teen fictional starter tasks dikhati hai.
- Customer, task, owner, due date aur status edit karne deti hai.
- Naya task add karne deti hai.
- Missing details aur invalid dates reject karti hai.
- Valid changes ek local CSV file mein save karti hai.
- App band karke dobara kholne par saved records load karti hai.

Abhi beginner version mein AI, login, reminders, charts ya dependencies nahi hain.
Pehle foundation samjhenge, phir ek feature ek baar add karenge.
Repository mein larger prototype bhi hai; abhi sirf basic files padhna.

## 4. Ek row ko samjho

Customer: ABC Company — kaam kis business ke liye hai?
Task: Set up the account — karna kya hai?
Owner: Abhinandan — responsible kaun hai?
Due date: 2026-10-09 — kab tak karna hai?
Status: Not started — abhi progress kya hai?

Owner yahan task karne wala insaan hai, company ka business owner zaroori nahi.
Done select karna user ka update hai; app actual setup complete hua ya nahi independently verify nahi karti.

## 5. Tools ka simple meaning

Python: instructions likhne ki programming language.
Streamlit: Python se browser mein form, table aur buttons banata hai.
Pandas: rows aur columns wali tables process karta hai.
DataFrame: Pandas ki table ka naam.
CSV: table save karne wali plain text file.
VS Code: editor jisme hum files padhenge, edit karenge aur code run karenge.
Terminal: jahan commands chalti hain aur app ke messages/errors aate hain.
Git: code ke changes aur saved checkpoints track karta hai.
GitHub: Git repository ko online host karta hai.
Commit: code ka named checkpoint.
Push: local commits GitHub par bhejna.

VS Code code edit karta hai; app ka actual screen browser mein khulta hai.

## 6. VS Code mein kaise kholna aur chalana hai?

1. VS Code kholo.
2. File > Open Workspace from File choose karo.
3. Onboarding-Copilot.code-workspace select karo.
   Yeh file isi project folder mein hai.
4. Sabse pehle basic_app.py kholo.
5. Terminal > Run Task > Run beginner tracker choose karo.
6. Terminal mein aaya Local URL browser mein kholo, normally http://localhost:8501.
7. App chalne tak terminal ko running rehne do.
8. Band karne ke liye us terminal mein Ctrl+C dabao.
   Windows confirmation aaye toh Y press karo.

Run Task existing Start.cmd use karta hai. Python extension ke bina bhi yeh route chal sakta hai.
Agar workspace trust prompt aaye, apni known project files review karke decision lena.

Alternative: Python aur Python Debugger extensions installed hon toh Run and Debug mein
Run beginner tracker choose karke F5 press karo.
VS Code mein Python: Select Interpreter se interpreter choose kar sakte ho.

Is computer par installed interpreter:
E:\job\placement-projects\.venv\Scripts\python.exe

Agar repo kisi doosre computer par clone karte ho:
Python 3.12 install hona chahiye. Setup.cmd chalao.
Phir Python: Select Interpreter se repo ki .venv\Scripts\python.exe select karo.
Workspace ka default interpreter existing parent environment ke liye configured hai;
new machine par local interpreter select karna hoga.

IMPORTANT: basic_app.py ko plain python basic_app.py se run mat karna.
Streamlit app ko python -m streamlit run basic_app.py command chahiye.
Run Task aur F5 configuration yahi karte hain.
Full prototype chalana ho toh Start-Advanced.cmd use karo.

## 7. Kaunsi files padhni hain?

basic_app.py: screen, table, input form aur buttons.
basic_storage.py: load, validate aur save.
data/basic_tasks.csv: tumhare saved records; first run par banegi.
docs/BEGINNER_GUIDE_HINGLISH.md: yeh explanation.

app.py, core.py aur integrations.py larger prototype ke files hain.
Unhe abhi padhne ki zarurat nahi.

## 8. App ke andar data kaise move hota hai?

App opens -> load_tasks() -> CSV read -> Pandas table -> editable screen.

User edit karta hai -> Save changes -> check_tasks() ->
valid hua toh CSV write -> screen refresh.

Invalid data -> error -> previous saved file unchanged.

Add task -> form ki values se ek row ->
existing rows ke saath combine -> validate -> save -> refresh.

## 9. Chhote programming concepts

Variable: kisi value ka naam, jaise owner = "Abhinandan".
List: values ka collection, jaise ["Not started", "In progress", "Done"].
Function: ek named kaam, jaise load_tasks().
Parameter: function ko diya gaya input.
Return: function se milne wala result.
If: condition true hone par specific code chalana.
For loop: har item par same kaam repeat karna.
Import: library ya doosri file ka code use karna.
Exception: error ko handle karna taaki user ko useful message mile.

check_tasks(table) mein table input hai.
Function required values aur dates check karke cleaned table return karta hai.

## 10. Do files kyun?

Screen code aur storage code alag responsibility rakhte hain.
Isse samajhna aur testing aasaan hai.
UI badal sakti hai aur save logic reuse ho sakta hai.

CSV kyun?
Chhote local project mein setup simple hai.
Multiple users ke simultaneous edits ke liye database chahiye.
Temporary CSV write karke replace karna incomplete write ka risk kam karta hai;
yeh multi-user concurrency solve nahi karta.

## 11. Future mein kya add karenge?

Stage 1: current basic tracker ko samajhna.
Stage 2: overdue label — due date nikal gayi aur task Done nahi hai.
Stage 3: customer/status filters aur completed task count.
Stage 4: task IDs, duplicate checks aur dependencies.
Stage 5: approved FAQs se answer aur unsupported question ki human queue.
Stage 6: meeting notes se proposed actions, save se pehle human review.
Stage 7: optional Claude API aur Google Sheets connections.
Stage 8: database, login, permissions, backups aur change history.

Yeh learning roadmap hai. Kuch features larger prototype mein already present hain;
hum basic version mein unhe samajhte hue introduce karenge.
AI add karne se pehle data aur business rules correct hone chahiye.
Automatic emails/reminders ke liye recipients, consent aur delivery behavior define karna hoga.

## 12. Interview mein kya bol sakte ho?

Problem:
Customer onboarding ke tasks aur follow-ups different places par hote hain.

Solution:
Maine tracker banaya jo customer, task, owner, due date aur status ek jagah rakhta hai.

Technical flow:
Streamlit UI input leti hai. Pandas table handle karta hai. Validation ke baad CSV mein save hota hai.

Limitation:
Current beginner version local single-user prototype hai.

Future:
Overdue flags, dependencies, FAQ assistance aur database-backed multi-user support.

Sirf woh features aur integrations tested kehna jo tumne khud run karke verify kiye hain.
Basic tracker ko AI-powered mat kehna; AI later stage/optional advanced mode mein hai.

## 13. Pehli practice

1. App kholo.
2. Hold the kickoff meeting ka status Done karo.
3. Save changes dabao.
4. App restart karke confirm karo ki Done saved hai.
5. Send welcome email naam ka task add karo.
6. Explain karo: data input kahan aaya, validation kahan hui, save kahan hua?

Next session mein basic_app.py ke imports aur first few lines se shuru karenge.
