import threading

task_status = {}       # task_id -> "queued" / "processing" / "completed" / "error"
task_result = {}       # task_id -> transcribed_text or error
task_lock = threading.Lock()