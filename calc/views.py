from django.shortcuts import render, redirect
from .models import Signup, HealthProfile, DailyEntry
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')


def get_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return Signup.objects.get(id=user_id)


# ---------------- SIGNUP ----------------
def signup(request):
    if request.method == "POST":

        name = request.POST.get("fullname")
        email = request.POST.get("email")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        Signup.objects.create(
            name=name,
            email=email,
            password=password,
            age=age,
            gender=gender,
            
        )

        return redirect("login")

    return render(request, "signup.html")


# ---------------- LOGIN ----------------
def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Signup.objects.get(email=email, password=password)

            request.session['user_id'] = user.id
            request.session['user_email'] = user.email

            return redirect('Profile')

        except Signup.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})
        
    return render(request, "login.html")


# ---------------- LOGOUT ----------------
def logout(request):
    request.session.flush()
    return redirect('login')


# ---------------- Profile----------------

def Profile(request):

    user = get_user(request)
    if not user:
        return redirect('login')

    report = HealthProfile.objects.filter(user=user).last()

    entries = DailyEntry.objects.filter(user=user).order_by('-date')[:7]
    entries = entries[::-1]

    labels = []
    steps = []
    water = []
    calories = []

    for e in entries:
        labels.append(str(e.date))
        steps.append(e.steps)
        water.append(e.water_intake)
        calories.append(e.calorie_intake)


    STEP_GOAL = 10000
    WATER_GOAL = 2.5
    CAL_MIN = 1000
    CAL_MAX = 2500

    # ---------------- DEFAULT VALUES ----------------
    bmi = None
    bmi_status = "Unknown"
    health_score = 0
    health_status = "No Health Data"
    tasks = []

  
    if report and report.bmi is not None:

        bmi = report.bmi

        if bmi < 18.5:
            bmi_status = "Underweight"

        elif bmi < 25:
            bmi_status = "Healthy"

        elif bmi < 30:
            bmi_status = "Overweight"

        else:
            bmi_status = "Obese"

    # ---------------- HEALTH SCORE + STATUS ----------------
    if entries and report:

        latest = entries[-1]

        health_score = calculate_health_score(latest, bmi_status)

      
        if health_score >= 80:
            health_status = "Excellent 👍"

        elif health_score >= 60:
            health_status = "Good 😊"

        elif health_score >= 40:
            health_status = "Average ⚠️"

        else:
            health_status = "Poor ❌"

        # ---------------- SMART TASK SYSTEM ----------------

        if latest.steps < STEP_GOAL:
            tasks.append(f"Walk {STEP_GOAL - latest.steps} more steps today")

        if latest.water_intake < WATER_GOAL:
            tasks.append(f"Drink {WATER_GOAL - latest.water_intake:.1f}L more water")

        if latest.calorie_intake < CAL_MIN:
            tasks.append("Eat more nutritious calories today")

        elif latest.calorie_intake > CAL_MAX:
            tasks.append("Reduce excess calorie intake (avoid junk food)")

    return render(request, "profile.html", {
        "user": user,
        "report": report,

        # chart data
        "labels": labels,
        "steps": steps,
        "water": water,
        "calories": calories,

        # health data
        "bmi": bmi,
        "bmi_status": bmi_status,
        "health_score": health_score,
        "health_status": health_status,
        "tasks": tasks
    })
# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html')


# ---------------- FEATURE ----------------
def feature(request):
    return render(request, 'feature.html')


# ---------------- PERSONAL HEALTH  DETAILS ----------------
def personal(request):

    user = get_user(request)
    if not user:
        return redirect('login')

    report, created = HealthProfile.objects.get_or_create(user=user)

    if request.method == "POST":

        age = int(request.POST.get("age"))
        height = float(request.POST.get("height")) / 100
        weight = float(request.POST.get("weight"))
        bp = int(request.POST.get("bp"))
        sugar = float(request.POST.get("sugar"))

        bmi = round(weight / (height * height), 2)

        report.age = age
        report.height = height * 100
        report.weight = weight
        report.bp = bp
        report.sugar = sugar
        report.bmi = bmi
        report.save()

        return redirect('personal')

    return render(request, "personal.html", {
        "user": user,
        "report": report
    })
# ---------------- DAILY ENTRY ----------------
def daily_entry(request):

    user = get_user(request)
    if not user:
        return redirect('login')

    if request.method == "POST":
        date = request.POST['date']
        steps = int(request.POST['steps'])
        water = float(request.POST['water'])
        calories = int(request.POST['calories'])

        DailyEntry.objects.create(
            user=user,
            date=date,
            steps=steps,
            water_intake=water,
            calorie_intake=calories
        )

        return redirect('daily_task')

    return render(request, "daily_entry.html", {"user": user})


# ---------------- HEALTH SCORE ----------------
def calculate_health_score(entry, bmi_status):

    score = 0

    if entry.steps >= 10000:
        score += 25
    elif entry.steps >= 7000:
        score += 20
    else:
        score += 15

    if entry.water_intake >= 2.5:
        score += 25
    elif entry.water_intake >= 2:
        score += 20
    else:
        score += 15

    if 1800 <= entry.calorie_intake <= 2200:
        score += 25
    else:
        score += 15

    if bmi_status == "Normal":
        score += 25
    else:
        score += 15

    return score


# ---------------- DAILY TASK ----------------
def daily_task(request):

    user = get_user(request)
    if not user:
        return redirect('login')

    entries = DailyEntry.objects.filter(user=user).order_by('date')
    report = HealthProfile.objects.filter(user=user).last()

    labels, steps, water, calories = [], [], [], []

    for e in entries:
        labels.append(str(e.date))
        steps.append(e.steps)
        water.append(e.water_intake)
        calories.append(e.calorie_intake)

    health_score = 0
    health_status = ""
    tasks = []

    if entries.exists() and report:

        latest = entries.last()

        # ---------------- HEALTH SCORE ----------------
        health_score = calculate_health_score(latest, "Normal")

        if health_score >= 80:
            health_status = "Excellent 👍"
        elif health_score >= 60:
            health_status = "Good 😊"
        elif health_score >= 40:
            health_status = "Average ⚠️"
        else:
            health_status = "Poor ❌"

        # ---------------- STEP TASK ----------------
        if latest.steps < 10000:
            tasks.append(f"Walk {10000 - latest.steps} steps")

        # ---------------- WATER TASK ----------------
        if latest.water_intake < 2.5:
            tasks.append(f"Drink {2.5 - latest.water_intake:.1f}L water")

        # ---------------- BMI BASED CALORIE LOGIC ----------------
        bmi = report.bmi if report else 0

        if bmi:
            if bmi < 18.5:
                if latest.calorie_intake < 2000:
                    tasks.append("You are underweight → increase calories (healthy diet ~2000+ kcal)")
                else:
                    tasks.append("Maintain high-calorie nutritious diet")

            elif 18.5 <= bmi <= 24.9:
                if latest.calorie_intake < 1800:
                    tasks.append("Maintain balanced diet (1800–2200 kcal)")
                elif latest.calorie_intake > 2200:
                    tasks.append("Slightly reduce calorie intake")
                else:
                    tasks.append("Calorie intake is balanced")

            elif bmi >= 25:
                if latest.calorie_intake > 1000:
                    tasks.append("Overweight → reduce calorie intake (avoid junk food)")
                else:
                    tasks.append("Maintain controlled calorie diet")

    return render(request, "Profile.html", {
        "user": user,
        "labels": labels,
        "steps": steps,
        "water": water,
        "calories": calories,
        "health_score": health_score,
        "health_status": health_status,
        "tasks": tasks
    })
def health_stat(request):

    user = get_user(request)
    if not user:
        return redirect('login')

    report = HealthProfile.objects.filter(user=user).order_by('-id').first()

    bmi = report.bmi if report else 0
    bp = report.bp if report else 0
    sugar = report.sugar if report else 0

    suggestion = []

    if bmi:
        if bmi > 24.9:
            suggestion.append("BMI is high → reduce calories and increase exercise")
        elif bmi < 18.5:
            suggestion.append("BMI is low → improve diet and nutrition")
        else:
            suggestion.append("BMI is normal → maintain your routine")

    if bp:
        if bp > 130:
            suggestion.append("Blood pressure is high → reduce salt intake")
        elif bp < 90:
            suggestion.append("Blood pressure is low → consult doctor")
        else:
            suggestion.append("BP is normal")

    if sugar:
        if sugar > 140:
            suggestion.append("Sugar is high → avoid sweets and carbs")
        elif sugar < 70:
            suggestion.append("Sugar is low → eat timely meals")
        else:
            suggestion.append("Sugar is normal")

    return render(request, "health_stat.html", {
        "report": report,
        "bmi": bmi,
        "bp": bp,
        "sugar": sugar,
        "suggestion": suggestion
    })