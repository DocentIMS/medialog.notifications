$(document).ready(function () {
    function initFilters() {
        var usersFilterCheckbox = $("#form-widgets-user_filter-0");
        var timeFilterCheckbox = $("#form-widgets-time_filter-0");

        var fields = {
            users: [
                $("#formfield-form-widgets-notify_users"),
                $("#formfield-form-widgets-notify_groups"),
                $("#formfield-form-widgets-additional_users")
            ],
            time: [
                $("#formfield-form-widgets-relative_time"),
                $("#formfield-form-widgets-effective_date")
            ]
        };

        function toggleFields(checkbox, fieldsGroup) {
            fieldsGroup.forEach(field => field.toggle(!checkbox.is(":checked")));
        }

        // Initialize visibility
        toggleFields(usersFilterCheckbox, fields.users);
        toggleFields(timeFilterCheckbox, fields.time);

        // Attach event listeners only once
        usersFilterCheckbox.off("change").on("change", () => toggleFields(usersFilterCheckbox, fields.users));
        timeFilterCheckbox.off("change").on("change", () => toggleFields(timeFilterCheckbox, fields.time));
    }

    // Initialize on page load
    initFilters();

    // Use MutationObserver to handle dynamically added form fields
    const observer = new MutationObserver(() => {
        initFilters();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
