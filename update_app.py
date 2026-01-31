# Add this to your main app.py file

# Add to imports section:
from routes import opposition

# Add after other router includes:
app.include_router(opposition.router)

# Add route for opposition monitor page:
@app.get('/opposition')
async def opposition_monitor(request: Request):
    return templates.TemplateResponse('opposition.html', {'request': request})