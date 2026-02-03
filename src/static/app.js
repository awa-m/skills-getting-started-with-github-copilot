document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // --- 参加者リストのHTML生成 ---
        let participantsHTML = "";
        if (details.participants.length > 0) {
          participantsHTML = `
            <div class="participants-section">
              <strong>Participants:</strong>
              <ul class="participants-list"></ul>
            </div>
          `;
        } else {
          participantsHTML = `
            <div class="participants-section">
              <strong>Participants:</strong>
              <span class="no-participants">No participants yet</span>
            </div>
          `;
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHTML}
        `;

        // 参加者リストに削除ボタンを追加
        if (details.participants.length > 0) {
          const ul = activityCard.querySelector(".participants-list");
          details.participants.forEach(email => {
            const li = document.createElement("li");
            li.style.display = "flex";
            li.style.alignItems = "center";

            const nameSpan = document.createElement("span");
            nameSpan.textContent = email;
            nameSpan.style.flexGrow = "1";

            const deleteBtn = document.createElement("button");
            deleteBtn.innerHTML = "🗑️";
            deleteBtn.title = "登録解除";
            deleteBtn.style.marginLeft = "8px";
            deleteBtn.style.background = "none";
            deleteBtn.style.border = "none";
            deleteBtn.style.cursor = "pointer";
            deleteBtn.style.fontSize = "1.1em";

            deleteBtn.addEventListener("click", async () => {
              if (confirm(`本当に ${email} を「${name}」から登録解除しますか？`)) {
                const res = await fetch(`/activities/${encodeURIComponent(name)}/unregister?email=${encodeURIComponent(email)}`, { method: "DELETE" });
                if (res.ok) {
                  await fetchActivities();
                } else {
                  alert("登録解除に失敗しました");
                }
              }
            });

            li.appendChild(nameSpan);
            li.appendChild(deleteBtn);
            ul.appendChild(li);
          });
        }

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // 参加登録成功時にアクティビティリストを再取得
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
  document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('registration-form');
      const input = document.getElementById('participant-name');
      const list = document.getElementById('participants-list');

      // Hide bullet points via JS in case CSS is not enough
      list.style.listStyleType = 'none';

      form.addEventListener('submit', function(event) {
          event.preventDefault();
          const name = input.value.trim();
          if (name) {
              const li = document.createElement('li');
              li.style.display = 'flex';
              li.style.alignItems = 'center';

              const nameSpan = document.createElement('span');
              nameSpan.textContent = name;
              nameSpan.style.flexGrow = '1';

              const deleteBtn = document.createElement('button');
              deleteBtn.innerHTML = '🗑️';
              deleteBtn.title = '削除';
              deleteBtn.style.marginLeft = '8px';
              deleteBtn.style.background = 'none';
              deleteBtn.style.border = 'none';
              deleteBtn.style.cursor = 'pointer';
              deleteBtn.style.fontSize = '1.1em';

              deleteBtn.addEventListener('click', function() {
                  list.removeChild(li);
              });

              li.appendChild(nameSpan);
              li.appendChild(deleteBtn);
              list.appendChild(li);
              input.value = '';
          }
      });
  });
