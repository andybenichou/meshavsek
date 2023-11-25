# Meshavshek: Advanced Guard Scheduling Solution

Welcome to Meshavshek, a sophisticated tool designed to streamline the complexities of guard scheduling. Meshavshek aligns guard schedules with individual preferences and availability, ensuring an efficient and balanced approach to guard planning.

## Key Features

- **Guard Duo Choices:** Ability to select preferred guard pairs for shifts.
- **Same-Times Guard Preferences:** Option to schedule certain guards simultaneously, subject to availability.
- **Flexible Planning:** Accommodates individual guard preferences for specific spots and time-offs.
- **Dynamic Adjustments:** Intelligent algorithm that adapts to various scheduling constraints.

## Installation

Get started with Meshavshek in a few simple steps:
1. Clone the project repository: `git clone git@github.com:andybenichou/meshavsek.git`
2. Navigate to the project directory. You will find:
    - Configuration templates in the root directory. Copy, paste, and rename these by removing the '.template' extension.
    - Input templates in the `data` folder. Use these templates to input guard details and preferences.

## Configuration and Usage

### Setting Up Meshavshek
Customize your scheduling setup in the `config.py` and `guards_config.py` files:
- **Randomness Level (1-10):** Introduces variability in pairing guards to prevent repetitive patterns. Note that higher randomness may impact planning efficiency.
- **Minimal Delay:** Start with a higher delay between shifts for each guard and decrease it gradually to optimize the schedule.
- **Partner Availability Delay:** Define the minimum delay required to consider a guard's partner available for a shared shift.
- Additional parameters are available for a tailored scheduling experience.

### Running Meshavshek
Execute the `main.py` script and follow the prompts:
- Enter `0` to schedule up to the last day included in your input data.
- Enter `-1` to view insights about the current planning state.
- Enter a positive number to initiate the scheduling process.

### Optimization Tips
- Fine-tune the `MINIMAL_DELAY` setting to balance scheduling efficiency with guard availability. If the program frequently encounters dead ends (indicated by repeated 'Oh oh, we got ourselves into a cul-de-sac...' messages toi many times), consider decreasing this delay.
- Utilize a higher `RETRIES_NUM_BEFORE_CRASH` value for more thorough planning attempts and better outcome.

## Support and Feedback
For assistance, feedback, or discussions about scheduling strategies, feel free to contact me, Andy Benichou, at `andybenichou@gmail.com`.

## License
Meshavshek is licensed under a Custom License for Private Use. Redistribution and commercial use are not permitted without explicit permission from the owner. Private, non-commercial use is allowed under specific conditions.

For detailed terms, refer to the [LICENSE](LICENSE) file in the project repository.

## Acknowledgments
Special thanks to all the guards whose hard work and dedication inspired the creation of Meshavshek. This tool is dedicated to making guard scheduling more efficient and user-friendly.

---

Meshavshek: Streamlining guard scheduling with precision and efficiency.
