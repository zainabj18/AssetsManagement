def test_init_db(flask_app):
    with flask_app.app_context():
        runner = flask_app.test_cli_runner()
        result = runner.invoke(args=['init-db'])
        assert result.exit_code == 0
        assert 'Database intialised' in result.output

