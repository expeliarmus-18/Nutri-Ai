package com.toksh.NutriAi.repository;

import com.toksh.NutriAi.entt.User;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface UserRepository extends MongoRepository<User, ObjectId> {
    User findByEmail(String email);
}