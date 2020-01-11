get_contributions = """query GetContributions($username: String!) {
  user(login: $username) {
    name
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            weekday
          }
          firstDay
        }
      }
    }
  }
}"""