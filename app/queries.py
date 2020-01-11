get_contributions = """query GetContributions($username: String!) {
  user(login: $username) {
    name
    contributionsCollection {
      contributionCalendar {
        colors
        totalContributions
        weeks {
          contributionDays {
            color
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