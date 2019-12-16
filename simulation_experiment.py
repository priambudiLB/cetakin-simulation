import simpy
import numpy
from config_experiment import (
    OPEN_DURATION_MINUTES,
    IS_PRINTER_HYBRID,
    COMPUTER_CAPACITY,
    PRINT_DURATION_SCALE_MINUTES,
    EDIT_DURATION_SCALE_MINUTES,
    ONLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES,
    OFFLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES,
    HYBRID_PRINTER_CAPACITY,
    SIMULATION_NUMBER,
    ONLINE_PRINTER_CAPACITY,
    OFFLINE_PRINTER_CAPACITY,
)
from visualize import pie, bar
from customer import OnlineCustomer, OfflineCustomer
from resource import MonitoredResource


def average(array):
    return sum(array) / len(array)


def run_cetakin_simulation(number_of_simulation):
    service_rates = []
    average_queue_times = []
    customer_serveds = []
    online_printer_utilizations = []
    offline_printer_utilizations = []
    computer_utilizations = []
    online_printer_queue_probabilities = []
    offline_printer_queue_probabilities = []
    computer_queue_probabilities = []
    average_online_printer_queue_durations = []
    average_offline_printer_queue_durations = []
    average_computer_queue_durations = []

    for i in range(number_of_simulation):
        env = simpy.Environment()

        computer = MonitoredResource(env, capacity=COMPUTER_CAPACITY)
        offline_current_time = 0
        offline_customer_number = 1
        offline_printer = MonitoredResource(env, capacity=OFFLINE_PRINTER_CAPACITY)
        while offline_current_time < OPEN_DURATION_MINUTES:
            OfflineCustomer(
                env,
                "Offline Customer %d" % offline_customer_number,
                offline_printer,
                offline_current_time,
                computer,
            )
            offline_current_time += numpy.random.exponential(
                OFFLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES
            )
            offline_customer_number += 1

        online_current_time = 0
        online_customer_number = 1
        online_printer = MonitoredResource(env, capacity=ONLINE_PRINTER_CAPACITY)
        while online_current_time < OPEN_DURATION_MINUTES:
            OnlineCustomer(
                env,
                "Online Customer %d" % online_customer_number,
                online_printer,
                online_current_time,
            )
            online_current_time += numpy.random.exponential(
                ONLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES
            )
            online_customer_number += 1

        env.run()
        customer_served = offline_customer_number + online_customer_number
        service_rate = customer_served / OPEN_DURATION_MINUTES

        service_rates.append(service_rate)
        customer_serveds.append(customer_served)
        online_printer_utilizations.append(online_printer.utilization)
        offline_printer_utilizations.append(offline_printer.utilization)
        computer_utilizations.append(computer.utilization)
        computer_queue_probabilities.append(computer.queue_probability)
        offline_printer_queue_probabilities.append(offline_printer.queue_probability)
        online_printer_queue_probabilities.append(online_printer.queue_probability)
        average_computer_queue_durations.append(computer.queue_duration)
        average_online_printer_queue_durations.append(online_printer.queue_duration)
        average_offline_printer_queue_durations.append(offline_printer.queue_duration)

    return (
        average(service_rates),
        average(customer_serveds),
        average(online_printer_utilizations),
        average(offline_printer_utilizations),
        average(computer_utilizations),
        average(offline_printer_queue_probabilities),
        average(online_printer_queue_probabilities),
        average(computer_queue_probabilities),
        average(average_computer_queue_durations),
        average(average_online_printer_queue_durations),
        average(average_offline_printer_queue_durations),

    )


def run_hybrid_simulation(number_of_simulation):
    service_rates = []
    average_queue_times = []
    customer_serveds = []
    printer_utilizations = []
    computer_utilizations = []
    printer_queue_probabilities = []
    computer_queue_probabilities = []
    average_printer_queue_durations = []
    average_computer_queue_durations = []

    for i in range(number_of_simulation):
        env = simpy.Environment()

        printers = MonitoredResource(env, capacity=HYBRID_PRINTER_CAPACITY)
        computer = MonitoredResource(env, capacity=COMPUTER_CAPACITY)
        offline_current_time = 0
        offline_customer_number = 1
        offline_printer = printers
        while offline_current_time < OPEN_DURATION_MINUTES:
            OfflineCustomer(
                env,
                "Customer %d" % offline_customer_number,
                offline_printer,
                offline_current_time,
                computer,
            )
            offline_current_time += numpy.random.exponential(
                OFFLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES
            )
            offline_customer_number += 1

        online_current_time = 0
        online_customer_number = 1
        online_printer = printers
        while online_current_time < OPEN_DURATION_MINUTES:
            OnlineCustomer(
                env,
                "Customer %d" % online_customer_number,
                online_printer,
                online_current_time,
            )
            online_current_time += numpy.random.exponential(
                ONLINE_CUSTOMER_INTERARRIVAL_SCALE_MINUTES
            )
            online_customer_number += 1

        env.run()
        customer_served = offline_customer_number + online_customer_number
        service_rate = customer_served / OPEN_DURATION_MINUTES

        service_rates.append(service_rate)
        customer_serveds.append(customer_served)
        printer_utilizations.append(printers.utilization)
        computer_utilizations.append(computer.utilization)
        computer_queue_probabilities.append(computer.queue_probability)
        printer_queue_probabilities.append(printers.queue_probability)
        average_computer_queue_durations.append(computer.queue_duration)
        average_printer_queue_durations.append(printers.queue_duration)

    return (
        average(service_rates),
        average(customer_serveds),
        average(printer_utilizations),
        average(computer_utilizations),
        average(computer_queue_probabilities),
        average(printer_queue_probabilities),
        average(average_computer_queue_durations),
        average(average_printer_queue_durations)
    )


if __name__ == "__main__":
    if IS_PRINTER_HYBRID:
        (
            service_rate,
            customer_served,
            printer_utilization,
            computer_utilization,
            computer_queue_probability,
            printer_queue_probability,
            average_computer_queue_duration,
            average_printer_queue_duration
        ) = run_hybrid_simulation(SIMULATION_NUMBER)

        pie([
            "Printer Utilization",
            "Computer Utilization",
            "Printer Queue Probability",
            "Computer Queue Probability",
            ], 
            [
                printer_utilization,
            computer_utilization,
            printer_queue_probability,
                computer_queue_probability,
            
            ],
            [["Idle", "Busy"],["Queue", "No Queue"]],
            2
        )
        bar(
            "Average Queue Duration (The lower the better)"
            , 
            [
            average_printer_queue_duration,
            average_computer_queue_duration,
            ],
            ["Printer", "Computer"],
            "Duration (minutes)"
        )

        with open("result.txt", "a") as f:
            f.write("Service Rate: " + str(service_rate) + "\n")
            f.write("Jumlah Customer terlayani : " + str(customer_served) + "\n")
            f.write("Utilisasi Printer : " + str(printer_utilization) + "\n")
            f.write("Utilisasi Komputer : " + str(computer_utilization) + "\n")
            f.write(
                "Probabilitas queue Komputer : "
                + str(computer_queue_probability)
                + "\n"
            )
            f.write(
                "Probabilitas queue Printer : " + str(printer_queue_probability) + "\n"
            )
            f.write("Rata-rata waktu tunggu antrian komputer : " + str(average_computer_queue_duration) + "\n")
            f.write("Rata-rata waktu tunggu antrian printer : " + str(average_printer_queue_duration) + "\n")
            f.write("\n")

    else:
        (
            service_rate,
            customer_served,
            online_printer_utilization,
            offline_printer_utilization,
            computer_utilization,
            offline_printer_queue_probability,
            online_printer_queue_probability,
            computer_queue_probability,
            average_computer_queue_duration,
            average_online_printer_queue_duration,
            average_offline_printer_queue_duration,
        ) = run_cetakin_simulation(SIMULATION_NUMBER)

        pie([
            "Online Printer Utilization",
            "Offline Printer Utilization",
            "Computer Utilization",
            "Online Printer Queue Probability",
            "Offline Printer Queue Probability",
            "Computer Queue Probability",
            ], 
            [
                online_printer_utilization,
                offline_printer_utilization,
                computer_utilization,
                online_printer_queue_probability,
                offline_printer_queue_probability,
                computer_queue_probability,
            ],
            [["Idle", "Busy"],["Queue", "No Queue"]],
            3
        )
        bar(
            "Average Queue Duration (The lower the better)"
            , 
            [
            average_online_printer_queue_duration,
            average_offline_printer_queue_duration,
            average_computer_queue_duration,
            ],
            ["Online Printer", "Offline Printer", "Computer"],
            "Duration (minutes)"
        )
        with open("result.txt", "a") as f:
            f.write("Service Rate: " + str(service_rate) + "\n")
            f.write("Jumlah Customer terlayani : " + str(customer_served) + "\n")
            f.write(
                "Utilisasi Printer Online : " + str(online_printer_utilization) + "\n"
            )
            f.write(
                "Utilisasi Printer Offline : " + str(offline_printer_utilization) + "\n"
            )
            f.write("Utilisasi Komputer : " + str(computer_utilization) + "\n")
            f.write("Probabilitas Antri Printer Offline : " + str(offline_printer_queue_probability) + "\n")
            f.write("Probabilitas Antri Printer Online : " + str(online_printer_queue_probability) + "\n")
            f.write("Probabilitas Antri Komputer : " + str(computer_queue_probability) + "\n")
            f.write("Rata-rata Waktu tunggu Antrian Komputer : " + str(average_computer_queue_duration) + "\n")
            f.write("Rata-rata waktu tunggu Antri printer online : " + str(average_online_printer_queue_duration) + "\n")
            f.write("Rata-rata waktu tunggu Antri printer offline : " + str(average_offline_printer_queue_duration) + "\n")
            f.write("\n")
