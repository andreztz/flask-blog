def config(app):
    @app.template_filter("date_format")
    def date_format(timestamp):
        def suffix(d):
            return (
                "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")
            )

        def custom_format(format, t):
            return t.strftime(format).replace("{S}", str(t.day) + suffix(t.day))

        return custom_format("%B {S}, %Y", timestamp)
