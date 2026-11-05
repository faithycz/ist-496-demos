import asyncio
from agents import Runner, trace
from sales_agent.sales_agents import sales_picker, sales_sender, multi_sales_manager
from sales_agents import sales_agent1, sales_agent2, sales_agent3

async def write_sales_emails(message: str) -> list[str]:
    """
    Runs three sales agents in parallel and returns their written emails.

    :param message: The basis for the email message to be sent by the agents.
    :return: A list of emails sent by the agents.
    """

    with trace("Sales email generation"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )

        outputs = [result.final_output for result in results]

        return outputs

async def select_best_email(emails: list[str]) -> str:
    """
    Provides the generated sales emails from the agents to the sales picker and returns the best email.

    :param emails: A list of emails to be evaluated.
    :return: The best sales email.
    """

    emails_list = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(emails)

    with trace("Sales email selection"):
        result = await Runner.run(sales_picker, emails_list)

        return result.final_output

async def send_best_email(emails: list[str]) -> str:
    """
    Provides the generated sales emails from the agents to the sales sender, which picks and sends the best email.

    :param emails: A list of emails to be evaluated.
    :return: The best sales email.
    """

    emails_list = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(emails)

    with trace("Sales email selection and sending"):
        result = await Runner.run(sales_sender, emails_list)

        return result.final_output

async def use_multi_manager() -> str:
    """
    Runs the multi-sales manager using multiple sales agents from different LLMS.

    :return: The final output from the multi-sales manager.
    """

    task = """
    Follow these steps:

    1. Generate Drafts: Use each of the three sales_agent tools to generate different email drafts.
    Just instruct each to write a sales email; no further details are needed.
    Do not proceed until all three drafts are ready, one from each tool.

    2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.

    3. Use your tool to send the best email (and only the best email) to the user. Only send 1 email.
    """

    with trace("Sales Manager across different models"):
        result = await Runner.run(multi_sales_manager, task)

        return result.final_output