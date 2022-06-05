from tasks.models import Order


def reorder_queue():
    order = list(Order.objects.order_by('-order_number').all())
    tasks_priority = [task.task.priority for task in order]
    tasks_priority.sort(reverse=True)
    for order_number, task_priority in enumerate(tasks_priority):
        for task_index, task in enumerate(order):
            if task.task.priority == task_priority:
                task.order_number = order_number + 1
                task.save()
                order.pop(task_index)
