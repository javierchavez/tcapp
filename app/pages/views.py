from flask import Flask, render_template, request, redirect, url_for, session



from app.app_and_db import app



# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('pages/home_page.html')


@app.route('/member')
def member_page():
    return render_template('pages/member_page.html')

@app.route('/admin')
def admin_page():
    return render_template('pages/admin_page.html')
