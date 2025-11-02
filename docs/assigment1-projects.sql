-- get the names of the running Projects
SELECT p.Name 
FROM project p
JOIN Employee e ON p.IdEmployee = e.IdEmployee
JOIN Company c ON p.IdCompany = c.IdCompany
WHERE p.FinishedAt IS NULL

-- get the number of finished Projects per Company
SELECT
c.IdCompany,
c.Name,
COUNT(*) FinishedProjectCount
FROM project p
JOIN Employee e ON p.IdEmployee = e.IdEmployee
JOIN Company c ON p.IdCompany = c.IdCompany
WHERE p.FinishedAt IS NOT NULL
GROUP BY c.IdCompany, c.Name
ORDER BY FinishedProjectCount DESC

-- get the Company Names that have 2 or more different Projects with the same Name
SELECT DISTINCT c.Name
FROM(
    SELECT e.IdCompany, p.Name, COUNT(DISTINCT p.IdProject) AS ProjectCount
    FROM project p
    JOIN Employee e ON p.IdEmployee = e.IdEmployee
    JOIN Company c ON p.IdCompany = c.IdCompany
    GROUP BY e.IdCompany, p.Name
    HAVING COUNT(DISTINCT p.IdProject) >= 2
) AS ProjectCounts
JOIN Company c ON ProjectCounts.IdCompany = c.IdCompany