# test_goals.py

from main import save_or_update_goal, getAllGoalsWithProgress, getTotalSavingsProgress

def test_all_goal_functions():
    userid = "jdoe"

    # 1. Save or update a goal
    result1 = save_or_update_goal(userid, "School", 1500, "2026-06-01")
    assert result1 == True or isinstance(result1, dict), f"Save failed: {result1}"
    print("✅ saveCategoryGoal passed")

    # 2. Get all goals with progress
    goals = getAllGoalsWithProgress(userid)
    assert isinstance(goals, list), "Goals should be a list"
    assert all("ProgressPercent" in g for g in goals), "Missing progress data"
    print("✅ get_all_goals_with_progress passed")
    for g in goals:
        print(f"Goal: {g['Category']}, Progress: {g['ProgressPercent']}%")

    # 3. Get total savings progress
    total = getTotalSavingsProgress(userid)
    print("Returned total progress:", total)
    assert total is not None, "Total progress returned None"
    assert isinstance(total, float), "Total progress should be a float"

# Run the test
if __name__ == "__main__":
    test_all_goal_functions()