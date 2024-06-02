document.getElementById("toggleAll").addEventListener("click", function () {
  var allTasksTable = document.getElementById("allTasks");
  var toggleButton = document.getElementById("toggleAll");

  if (allTasksTable.style.display === "none") {
    allTasksTable.style.display = "table";
    toggleButton.textContent = "すべての予定を非表示する";
  } else {
    allTasksTable.style.display = "none";
    toggleButton.textContent = "すべての予定を表示する";
  }
});
