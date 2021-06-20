import random
from typing import Optional
from referee.consts import (
    GOAL_X_LIMIT,
    TIME_STEP,
    ROBOT_NAMES,
    GameEvents,
    Team,
    NeutralSpotDistanceType,
)
from referee.supervisor import RCJSoccerSupervisor


class RCJSoccerReferee(RCJSoccerSupervisor):
    def check_robots_in_penalty_area(self):
        """
        Check whether robots are violating rule not to stay in
        penalty area for longer period of time
        """
        for robot in ROBOT_NAMES:
            pos = self.robot_translation[robot]
            self.penalty_area_chck[robot].track(pos, self.time)

            if self.penalty_area_chck[robot].is_violating():
                self.eventer.event(
                    supervisor=self,
                    type=GameEvents.INSIDE_PENALTY_FOR_TOO_LONG.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    },
                )
                furthest_spot = self.get_unoccupied_neutral_spot(
                    NeutralSpotDistanceType.FURTHEST,
                    robot,
                )
                self.move_object_to_neutral_spot(robot, furthest_spot)
                self.reset_checkers(robot)

    def check_progress(self):
        """
        Check that the robots, as well as the ball, have made enough progress
        in their respective time intervals. If they did not, call "Lack of
        Progress".
        """
        for robot in ROBOT_NAMES:
            pos = self.robot_translation[robot]
            self.progress_chck[robot].track(pos)

            if not self.progress_chck[robot].is_progress(robot):
                self.eventer.event(
                    supervisor=self,
                    type=GameEvents.LACK_OF_PROGRESS.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    }
                )
                nearest_spot = self.get_unoccupied_neutral_spot(
                    NeutralSpotDistanceType.NEAREST,
                    robot,
                )
                self.move_object_to_neutral_spot(robot, nearest_spot)
                self.reset_checkers(robot)

        bpos = self.ball_translation.copy()
        self.progress_chck['ball'].track(bpos)
        if not self.progress_chck['ball'].is_progress('ball'):
            self.eventer.event(
                supervisor=self,
                type=GameEvents.LACK_OF_PROGRESS.value,
                payload={
                    "type": "ball"
                },
            )
            nearest_spot = self.get_unoccupied_neutral_spot(
                NeutralSpotDistanceType.NEAREST,
                "ball",
            )
            self.move_object_to_neutral_spot("ball", nearest_spot)
            self.reset_checkers("ball")

    def check_goal(self):
        """Check if goal is scored"""

        team_goal = None
        team_kickoff = None

        # ball in the blue goal
        if self.ball_translation[0] > GOAL_X_LIMIT:
            self.score_yellow += 1

            team_goal = self.team_name_yellow
            team_kickoff = Team.BLUE.value

        # ball in the yellow goal
        elif self.ball_translation[0] < -GOAL_X_LIMIT:
            self.score_blue += 1

            team_goal = self.team_name_blue
            team_kickoff = Team.YELLOW.value

        # If a goal was scored, redraw the scores, set the timers, log what
        # happened and set the proper team for kickoff.
        if team_goal and team_kickoff:
            self.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

            self.eventer.event(
                supervisor=self,
                type=GameEvents.GOAL.value,
                payload={
                    "team_name": team_goal,
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                },
            )

            # Let the team that did not score the goal have a kickoff.
            self.team_to_kickoff = team_kickoff

    def kickoff(self, team: Optional[str] = None):
        """Set up the kickoff by putting one of the robots of the team that is
        kicking off closer to the center point

        Args:
            team (str): The team that is kicking off. If the team is not
                specified, it will be chosen randomly.
        """
        if team not in (Team.BLUE.value, Team.YELLOW.value, None):
            raise ValueError(f"Unexpected team name {team}")

        seed = random.random()
        if not team:
            team = Team.BLUE.value if seed > 0.5 else Team.YELLOW.value

        robot_name = self.reset_team_for_kickoff(team)

        self.eventer.event(
            supervisor=self,
            type=GameEvents.KICKOFF.value,
            payload={
                "robot_name": robot_name,
                "team_name": team,
            },
        )

    def tick(self) -> bool:
        # On the very first tick, note that the match has started
        if self.time == self.match_time:
            self.eventer.event(
                supervisor=self,
                type=GameEvents.MATCH_START.value,
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                    "total_match_time": self.match_time,
                },
            )

        self.time -= TIME_STEP / 1000.0

        # On the very last tick, note that the match has finished
        if self.time < 0:
            self.eventer.event(
                supervisor=self,
                type=GameEvents.MATCH_FINISH.value,
                payload={
                    "total_match_time": self.match_time,
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                },
            )

            return False

        self.draw_time(self.time)
        self.draw_event_messages()

        # If we are currently not in the post-goal waiting period,
        # check if a goal took place, setup the waiting period and move the
        # robots to proper positions afterwards.
        if self.ball_reset_timer == 0:
            self.check_goal()
            self.check_progress()
            self.check_robots_in_penalty_area()
        else:
            self.ball_reset_timer -= TIME_STEP / 1000.0
            self.draw_goal_sign()

            # If the post-goal waiting period is over, reset the robots to
            # their starting positions
            if self.ball_reset_timer <= 0:
                self.reset_positions()
                self.ball_reset_timer = 0
                self.hide_goal_sign()
                self.kickoff(self.team_to_kickoff)

        return True
