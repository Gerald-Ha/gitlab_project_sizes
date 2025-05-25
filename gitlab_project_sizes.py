import requests
import csv
import sys

# ==== CONFIGURATION ====
GITLAB_URL = "https://your.gitlab.instance"  # Replace with your GitLab instance URL
PRIVATE_TOKEN = "YOUR_ACCESS_TOKEN"  # Insert your GitLab Access Token here
PER_PAGE = 100
THRESHOLD_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}


def get_projects():
    projects = []
    page = 1

    while True:
        url = f"{GITLAB_URL}/api/v4/projects?statistics=true&per_page={PER_PAGE}&page={page}"
        response = requests.get(url, headers=HEADERS, verify=False)

        if response.status_code != 200:
            print("❌ Error retrieving projects:", response.text)
            sys.exit(1)

        data = response.json()
        if not data:
            break

        projects.extend(data)
        page += 1

    return projects


def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:3.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"


def save_to_csv(projects):
    with open("gitlab_project_sizes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Project", "Total", "Repository", "LFS", "CI-Artifacts", "Wiki"])
        for project in projects:
            name = project.get("name_with_namespace", "???")
            stats = project.get("statistics", {})
            writer.writerow([
                name,
                stats.get("storage_size", 0),
                stats.get("repository_size", 0),
                stats.get("lfs_objects_size", 0),
                stats.get("job_artifacts_size", 0),
                stats.get("wiki_size", 0)
            ])
    print("\n💾 CSV file 'gitlab_project_sizes.csv' saved.")


def show_extended_info(projects):
    print("\n🔍 Extended information for top projects:\n")
    for project in sorted(projects, key=lambda p: p.get("statistics", {}).get("storage_size", 0), reverse=True)[:10]:
        name = project.get("name_with_namespace", "???")
        stats = project.get("statistics", {})
        total = stats.get("storage_size", 0)

        print(f"📁 {name}")
        print(f"  Total size:         {format_size(total)}")
        print(f"  Repository:         {format_size(stats.get('repository_size', 0))}")
        print(f"  LFS objects:        {format_size(stats.get('lfs_objects_size', 0))}")
        print(f"  CI Artifacts:       {format_size(stats.get('job_artifacts_size', 0))}")
        print(f"  Wiki:               {format_size(stats.get('wiki_size', 0))}")

        if total >= THRESHOLD_BYTES:
            print("  ⚠️ Warning: Project exceeds 2 GB!\n")
        else:
            print()


def main():
    print("📊 Fetching project sizes from GitLab...")
    projects = get_projects()

    results = []
    for project in projects:
        stats = project.get("statistics", {})
        total = stats.get("storage_size", 0)
        name = project.get("name_with_namespace", "???")
        results.append((total, name))

    print("\n📁 Top 20 projects by storage usage:")
    for size, name in sorted(results, reverse=True)[:20]:
        warn = " ⚠️" if size >= THRESHOLD_BYTES else ""
        print(f"{format_size(size):>10}  {name}{warn}")

    # Extended details
    answer = input("\n❓ Show extended details for the top 10 projects? (y/n): ").strip().lower()
    if answer == 'y':
        show_extended_info(projects)

    # Export CSV
    answer = input("\n💾 Save results as CSV file? (y/n): ").strip().lower()
    if answer == 'y':
        save_to_csv(projects)


if __name__ == "__main__":
    main()