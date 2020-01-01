function audit_build(option){
//agents
agents= [];
//root agents
root_agents= [];
//rules
rules = [];
//global list of completed courses 
taken = []

    let a_len = 0; 
    

	agents.push(new Agent(
		'prep-1',
		['%and', 'COM+SCI 1', 'COM+SCI 31', 'COM+SCI 32', 'COM+SCI 33', 'COM+SCI 35L']
		)
	);

	a_len = agents.length-1;
	agents[a_len].chk = check.bind(agents[a_len]);
	agents[a_len].upd = finish.bind(agents[a_len], 5, -1);

	agents.push(new Agent(
		'prep-2',
		['%and', 'MATH 31A', 'MATH 31B', 'MATH 32A', 'MATH 32B', 'MATH 33A', 'MATH 33B', 'MATH 61']
		)
	);

	a_len = agents.length-1;
	agents[a_len].chk = check.bind(agents[a_len]);
	agents[a_len].upd = finish.bind(agents[a_len], 7, -1);

	agents.push(new Agent(
		'prep-3',
		['%and', ['%and', 'PHYSICS 1A', 'PHYSICS 1B', 'PHYSICS 1C'], ['%or?one', 'PHYSICS 4AL', 'PHYSICS 4BL']]
		)
	);

	a_len = agents.length-1;
	agents[a_len].chk = check.bind(agents[a_len]);
	agents[a_len].upd = finish.bind(agents[a_len], 4, -1);

	agents.push(new Agent(
		'major-1',
		['%and', 'COM+SCI 111', 'COM+SCI 118', 'COM+SCI 131', 'COM+SCI M151B', 'COM+SCI M152A', 'COM+SCI 180', 'COM+SCI 181']
		)
	);

	a_len = agents.length-1;
	agents[a_len].chk = check.bind(agents[a_len]);
	agents[a_len].upd = finish.bind(agents[a_len], 7, -1);

	agents.push(new Agent(
		'major-2',
		['%or?one', 'C&EE 110', 'EC+ENGR 131A', 'MATH 170A', 'STATS 100A']
		)
	);

	a_len = agents.length-1;
	agents[a_len].chk = check.bind(agents[a_len]);
	agents[a_len].upd = finish.bind(agents[a_len], 1, -1);

	if (option['major-5'] == 'BIOENGR'){
		agents.push(new Agent(
			'major-5',
			['%and', 'BIOENGR 100', 'BIOENGR C101', 'BIOENGR C104', 'BIOENGR C105', 'BIOENGR C106', 'BIOENGR C107', 'BIOENGR 110', 'BIOENGR 120', 'BIOENGR 121', 'BIOENGR C131', 'BIOENGR C139A', 'BIOENGR C139B', 'BIOENGR CM140', 'BIOENGR CM145', 'BIOENGR C147', 'BIOENGR M153', 'BIOENGR C155', 'BIOENGR 165EW', 'BIOENGR 167L', 'BIOENGR C175', 'BIOENGR 176', 'BIOENGR 177A', 'BIOENGR 177B', 'BIOENGR CM178', 'BIOENGR C179', 'BIOENGR 180', 'BIOENGR 180L', 'BIOENGR M182', 'BIOENGR C183', 'BIOENGR M184', 'BIOENGR C185', 'BIOENGR CM186', 'BIOENGR CM187', 'CHEM 20B', 'LIFESCI 7A']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B', 'LIFESCI 7A']));
		agents[a_len].rules.push(subset_restriction.bind(agents[a_len],['%and', 'CHEM 20B', 'LIFESCI 7A']));
	}
	if (option['major-5'] == 'CH+ENGR'){
		agents.push(new Agent(
			'major-5',
			['%and', 'CH+ENGR 100', 'CH+ENGR 101A', 'CH+ENGR 101B', 'CH+ENGR 101C', 'CH+ENGR 102A', 'CH+ENGR 102B', 'CH+ENGR 103', 'CH+ENGR 104A', 'CH+ENGR 104B', 'CH+ENGR 104C', 'CH+ENGR 104CL', 'CH+ENGR 104D', 'CH+ENGR 106', 'CH+ENGR 107', 'CH+ENGR 108A', 'CH+ENGR 108B', 'CH+ENGR 109', 'CH+ENGR 110', 'CH+ENGR C111', 'CH+ENGR C112', 'CH+ENGR 113', 'CH+ENGR CM114', 'CH+ENGR C115', 'CH+ENGR C116', 'CH+ENGR C118', 'CH+ENGR C119', 'CH+ENGR C121', 'CH+ENGR C124', 'CH+ENGR C125', 'CH+ENGR CM127', 'CH+ENGR C128', 'CH+ENGR C135', 'CH+ENGR C140', 'CH+ENGR CM145', 'CH+ENGR M153', 'CH+ENGR 188', 'CH+ENGR 188SA', 'CH+ENGR 188SB', 'CH+ENGR 188SC', 'CH+ENGR 194', 'CH+ENGR 199', 'CHEM 20B']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B']));
	}
	if (option['major-5'] == 'C&EE'){
		agents.push(new Agent(
			'major-5',
			['%and', 'C&EE 102', 'C&EE 103', 'C&EE C104', 'C&EE C105', 'C&EE 108', 'C&EE 108L', 'C&EE 110', 'C&EE 120', 'C&EE 121', 'C&EE 123', 'C&EE 125', 'C&EE 128L', 'C&EE 129L', 'C&EE 130', 'C&EE 135A', 'C&EE 135B', 'C&EE M135C', 'C&EE 135L', 'C&EE C137', 'C&EE 137L', 'C&EE 140L', 'C&EE 141', 'C&EE 142', 'C&EE 142L', 'C&EE 143', 'C&EE 144', 'C&EE 147', 'C&EE 148', 'C&EE 150', 'C&EE 151', 'C&EE 152', 'C&EE 153', 'C&EE 154', 'C&EE 155', 'C&EE 156A', 'C&EE 156B', 'C&EE 157A', 'C&EE 157B', 'C&EE 157C', 'C&EE 157L', 'C&EE C159', 'C&EE 164', 'C&EE M165', 'C&EE M166', 'C&EE M166L', 'C&EE 170', 'C&EE 180', 'C&EE 181', 'C&EE C182', 'C&EE 188', 'C&EE 194', 'C&EE 199', 'CHEM 20B']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B']));
	}
	if (option['major-5'] == 'EC+ENGR'){
		agents.push(new Agent(
			'major-5',
			['%and', 'EC+ENGR 3', 'EC+ENGR 10', 'EC+ENGR 100', 'EC+ENGR 101A', 'EC+ENGR 101B', 'EC+ENGR 102', 'EC+ENGR 110', 'EC+ENGR 110H', 'EC+ENGR 110L', 'EC+ENGR 111L', 'EC+ENGR 112', 'EC+ENGR 113', 'EC+ENGR 113DA', 'EC+ENGR 113DB', 'EC+ENGR 114', 'EC+ENGR 115A', 'EC+ENGR 115AL', 'EC+ENGR 115B', 'EC+ENGR 115C', 'EC+ENGR 115E', 'EC+ENGR M116C', 'EC+ENGR M116L', 'EC+ENGR M119', 'EC+ENGR 121B', 'EC+ENGR 121DA', 'EC+ENGR 121DB', 'EC+ENGR 123A', 'EC+ENGR 123B', 'EC+ENGR 128', 'EC+ENGR 131A', 'EC+ENGR 132A', 'EC+ENGR 132B', 'EC+ENGR 133A', 'EC+ENGR 133B', 'EC+ENGR 134', 'EC+ENGR 141', 'EC+ENGR 142', 'EC+ENGR C143A', 'EC+ENGR M146', 'EC+ENGR C147', 'EC+ENGR M153', 'EC+ENGR 162A', 'EC+ENGR 163A', 'EC+ENGR 163C', 'EC+ENGR 163DA', 'EC+ENGR 163DB', 'EC+ENGR 164DA', 'EC+ENGR 164DB', 'EC+ENGR 170A', 'EC+ENGR 170B', 'EC+ENGR 170C', 'EC+ENGR M171L', 'EC+ENGR 173DA', 'EC+ENGR 173DB', 'EC+ENGR 176', 'EC+ENGR 180DA', 'EC+ENGR 180DB', 'EC+ENGR 183DA', 'EC+ENGR 183DB', 'EC+ENGR 184DA', 'EC+ENGR 184DB', 'EC+ENGR M185', 'EC+ENGR 188', 'EC+ENGR 188SA', 'EC+ENGR 188SB', 'EC+ENGR 188SC', 'EC+ENGR 189', 'EC+ENGR 194', 'EC+ENGR 199']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'MAT+SCI'){
		agents.push(new Agent(
			'major-5',
			['%and', 'MAT+SCI 104', 'MAT+SCI M105', 'MAT+SCI 110', 'MAT+SCI 110L', 'MAT+SCI 111', 'MAT+SCI 111L', 'MAT+SCI C112', 'MAT+SCI 120', 'MAT+SCI 121', 'MAT+SCI 121L', 'MAT+SCI 122', 'MAT+SCI 130', 'MAT+SCI 131', 'MAT+SCI 131L', 'MAT+SCI 132', 'MAT+SCI 140A', 'MAT+SCI 140B', 'MAT+SCI 141L', 'MAT+SCI 143A', 'MAT+SCI 143L', 'MAT+SCI 150', 'MAT+SCI 151', 'MAT+SCI 160', 'MAT+SCI 161', 'MAT+SCI 161L', 'MAT+SCI 162', 'MAT+SCI CM163', 'MAT+SCI 170', 'MAT+SCI 171', 'MAT+SCI CM180', 'CHEM 20B']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B']));
	}
	if (option['major-5'] == 'MECH&AE'){
		agents.push(new Agent(
			'major-5',
			['%and', 'MECH&AE 101', 'MECH&AE 102', 'MECH&AE 103', 'MECH&AE 105A', 'MECH&AE 105D', 'MECH&AE 107', 'MECH&AE 131A', 'MECH&AE C131G', 'MECH&AE 133A', 'MECH&AE 135', 'MECH&AE 136', 'MECH&AE C137', 'MECH&AE C138', 'MECH&AE CM140', 'MECH&AE 150A', 'MECH&AE 150B', 'MECH&AE 150C', 'MECH&AE C150G', 'MECH&AE C150P', 'MECH&AE C150R', 'MECH&AE 154A', 'MECH&AE 154B', 'MECH&AE 154S', 'MECH&AE 155', 'MECH&AE 156A', 'MECH&AE C156B', 'MECH&AE 157', 'MECH&AE 157A', 'MECH&AE 161A', 'MECH&AE 161B', 'MECH&AE 161C', 'MECH&AE 162A', 'MECH&AE 162D', 'MECH&AE 162E', 'MECH&AE 166A', 'MECH&AE 166C', 'MECH&AE M168', 'MECH&AE 169A', 'MECH&AE 171A', 'MECH&AE 171B', 'MECH&AE 172', 'MECH&AE 174', 'MECH&AE C175A', 'MECH&AE 181A', 'MECH&AE 182B', 'MECH&AE 182C', 'MECH&AE 183A', 'MECH&AE M183B', 'MECH&AE C183C', 'MECH&AE 185', 'MECH&AE C186', 'MECH&AE C187L', 'CHEM 20B']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B']));
	}
	if (option['major-5'] == 'COM+GEN'){
		agents.push(new Agent(
			'major-5',
			['%and', 'CHEM 20A', 'EE+BIOL 135', 'HUM+GEN C144', 'LIFESCI 7A', 'LIFESCI 7B', 'LIFESCI 7C', 'LIFESCI 107', 'MCD+BIO 144', 'MCD+BIO 172', 'PHYSCI 125', 'BIOMATH M203', 'BIOMATH M211', 'BIOSTAT M272', 'BIOSTAT M278', 'EE+BIOL M231', 'HUM+GEN 236A', 'HUM+GEN 236B', 'STATS M254']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

		agents[a_len].rules.push(not_used_for_other.bind(agents[a_len],['%and', 'CHEM 20B']));
	}
	if (option['major-5'] == 'COM+GEN'){
		agents.push(new Agent(
			'major-5',
			['%and', 'CH+ENGR 102A', 'CH+ENGR CM127', 'C&EE 151', 'C&EE 153', 'C&EE C159', 'EC+ENGR M185', 'ENVIRON M153', 'ENVIRON 157', 'ENVIRON 159', 'MECH&AE 105A', 'MECH&AE 133A', 'MECH&AE 135', 'MECH&AE 136', 'MECH&AE C137', 'MECH&AE 150C', 'CH+ENGR 223', 'MAT+SCI 252', 'MAT+SCI 298']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'ENGR+MATH'){
		agents.push(new Agent(
			'major-5',
			['%and', 'C&EE 103', 'C&EE 110', 'COM+SCI 112', 'COM+SCI 170A', 'COM+SCI 180', 'COM+SCI 181', 'EC+ENGR 102', 'EC+ENGR 133A', 'EC+ENGR 131A', 'MECH&AE 181A', 'MECH&AE 182B', 'MECH&AE 182C', 'MATH 61', 'MATH 110A', 'MATH 115A', 'MATH 131A', 'MATH 132', 'MATH 151A', 'MATH 164', 'MATH 167', 'MECH&AE 181A', 'MECH&AE 182B', 'MECH&AE 182C']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'ENGR+SCI'){
		agents.push(new Agent(
			'major-5',
			['%and', 'BIOENGR 100', 'BIOENGR C101', 'CH+ENGR 100', 'CH+ENGR 102A', 'C&EE 101', 'C&EE 103', 'C&EE 108', ['%or?one', 'COM+SCI 31', 'MECH&AE M20', 'C&EE M20'], 'COM+SCI 32', 'EC+ENGR 10', 'EC+ENGR 100', 'EC+ENGR 101A', ['%or?one', 'ENGR M101', 'MAT+SCI M105'], 'EC+ENGR 102', 'EC+ENGR 133A', 'MAT+SCI 104', 'MECH&AE 101', 'MECH&AE 102', 'MECH&AE 103', 'MECH&AE 105A']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'NANO'){
		agents.push(new Agent(
			'major-5.1',
			['%or?one', 'ENGR M101', 'MAT+SCI M105']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 1, 4);

		agents.push(new Agent(
			'major-5.2',
			['%and', ['%or?one', 'ENGR M103', 'ENGR C&EEM165'], 'EC+ENGR 128', 'MECH&AE M183B', 'MECH&AE C187L']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 2, 8);

		root_agents.push(new RootAgent(
			'major-5',
			['major-5.1', 'major-5.2']
			)
		);

		a_len = root_agents.length-1;
		root_agents[a_len].upd = finish_agent_subgrp.bind(root_agents[a_len], 3, -1, 2);
	}
	if (option['major-5'] == 'PREMED'){
		agents.push(new Agent(
			'major-5',
			['%and', 'CHEM 30BL', 'CHEM 153A', 'LIFESCI 7B', 'LIFESCI 7C', 'LIFESCI 107', 'PHYSICS 4BL', ['%or?one', 'BIOSTAT 100A', 'STATS 100A']]
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'TECH+MGMT'){
		agents.push(new Agent(
			'major-5',
			['%and', 'C&EE 170', 'ENGR 110', 'ENGR 111', 'ENGR 112', 'ENGR 113', 'ENGR 160', 'ENGR 163', 'ENGR 180', 'MGMT 108', 'MGMT 160', 'MGMT 161', 'MGMT 162', 'MGMT 180']
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
	if (option['major-5'] == 'URBN+PL'){
		agents.push(new Agent(
			'major-5',
			['%and', 'C&EE 180', 'C&EE 181', ['%or?one', 'URBN+PL M120', 'PUB+AFF M109'], 'URBN+PL 121', 'URBN+PL 130', 'URBN+PL CM137', 'URBN+PL 141', 'URBN+PL M150', ['%or?one', 'URBN+PL CM151', 'PUB+AFF M153']]
			)
		);

		a_len = agents.length-1;
		agents[a_len].chk = check.bind(agents[a_len]);
		agents[a_len].upd = finish.bind(agents[a_len], 3, 12);

	}
}