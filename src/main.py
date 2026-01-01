"""
Main entry point for Todo App Phase 2.
"""

import sys
from src import cli


def main():
    """Main application loop (Phase 3)."""
    try:
        while True:
            cli.display_menu()
            choice = cli.get_menu_choice()

            # Basic operations
            if choice == 1:
                cli.handle_add_task()
            elif choice == 2:
                cli.handle_view_tasks()
            elif choice == 3:
                cli.handle_mark_complete()
            elif choice == 4:
                cli.handle_delete_task()
            elif choice == 5:
                cli.handle_edit_task()
            # Search & filter
            elif choice == 6:
                cli.handle_search_tasks()
            elif choice == 7:
                cli.handle_filter_priority()
            elif choice == 8:
                cli.handle_filter_category()
            elif choice == 9:
                cli.handle_view_overdue()
            elif choice == 10:
                cli.handle_view_today_tasks()
            elif choice == 11:
                cli.handle_view_tomorrow_tasks()
            # Organization
            elif choice == 12:
                cli.handle_sort_tasks()
            elif choice == 13:
                cli.handle_set_due_date()
            elif choice == 14:
                cli.handle_add_edit_notes()
            elif choice == 15:
                cli.handle_view_task_details()
            elif choice == 16:
                cli.handle_add_subtask()
            elif choice == 17:
                cli.handle_set_dependencies()
            elif choice == 18:
                cli.handle_set_recurring()
            # Templates
            elif choice == 19:
                cli.handle_save_template()
            elif choice == 20:
                cli.handle_list_templates()
            elif choice == 21:
                cli.handle_create_from_template()
            # Bulk operations
            elif choice == 22:
                cli.handle_bulk_mark_complete()
            elif choice == 23:
                cli.handle_bulk_delete()
            elif choice == 24:
                cli.handle_archive_completed()
            elif choice == 25:
                cli.handle_view_archived()
            # Advanced
            elif choice == 26:
                cli.handle_statistics()
            elif choice == 27:
                cli.handle_undo()
            elif choice == 28:
                cli.handle_exit()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
