if __name__ == "__main__":
    from src.controllers.cli_controller import CLIController
    from src.config import Config
    import sys

    config = Config()
    controller = CLIController(config)
    
    if "--ui" in sys.argv:
        from src.ui.gradio_ui import launch_gradio
        launch_gradio(config)
    else:
        controller.run()